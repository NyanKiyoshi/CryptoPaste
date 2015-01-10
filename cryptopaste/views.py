# -*- coding: utf-8 -*-
# ==== CryptoPaste
# AUTHOR: NyanKiyoshi
# COPYRIGHT: 2015 - NyanKiyoshi
# URL: https://github.com/NyanKiyoshi/CryptoPaste/
# LICENSE: https://github.com/NyanKiyoshi/CryptoPaste/master/LICENSE
#
# This file is part of CryptoPaste under the MIT license. Please take awareness about this latest before doing anything!

from pyramid.response import Response
from pyramid.view import view_config
from cryptopaste.models import DBSession, UserPaste, Paste, Timeout, SubmissionRegulator, DecryptionAttempt
from cryptopaste.utils import AESCipher, flash_response
from pyramid.httpexceptions import HTTPBadRequest, HTTPSeeOther, HTTPServerError, HTTPForbidden
from re import match
from transaction import manager
from datetime import timedelta, datetime
from sqlalchemy.exc import OperationalError
import logging
from traceback import format_exc
from time import sleep


@view_config(route_name='home', renderer='index.mako')
def home(request):
    if request.method == 'POST':
        if ('content' not in request.POST) or request.POST['content'].__sizeof__() > 2000000:
            raise HTTPBadRequest

        regulator = DBSession.query(SubmissionRegulator).filter_by(address=request.remote_addr).first()
        if regulator:
            if not regulator.next_time <= datetime.utcnow():
                flash_response(request, 'Please wait 30 seconds between each paste.')
                return request.POST
        else:
            regulator = SubmissionRegulator(address=request.remote_addr)
            with manager:
                DBSession.add(regulator)

        if not request.POST['content'].strip():
            flash_response(request, 'the content don\'t must be blank.')
            return request.POST
        for k in [
            {
                'key': 'user',
                'length': [1, 80],
                'match': [r'^([a-zA-Z0-9]+)$', 'alphanumerics characters'],
            },
            {
                'key': 'burn',
                'length': None,
                'match': None,
            },
            {
                'key': 'encryption',
                'length': None,
                'match': None,
            },
            {
                'key': 'key',
                'length': [1, 500],
                'match': [
                    r'^([a-zA-Z0-9\-._]+)$',
                    'alphanumerics characters and the following characters a-zA-Z0-9_-.'
                ],
            },
        ]:
            if (not k['key'] in request.POST) or not request.POST[k['key']]:
                request.POST[k['key']] = None
                continue
            if k['length']:
                if not k['length'][0] <= len(request.POST[k['key']]) <= k['length'][1]:
                    flash_response(
                        request,
                        '{key} must be between {min} and {max}.'.format(
                            key=k['key'], min=k['length'][0], max=k['length'][1]
                        )
                    )
                    return request.POST
            if k['match']:
                if not match(k['match'][0], request.POST[k['key']]):
                    flash_response(
                        request,
                        '{key} must be only contain {requirements}.'.format(key=k['key'], requirements=k['match'][1])
                    )
                    return request.POST

        if 'expiration' not in request.POST:
            request.POST['expiration'] = timedelta(days=36500)  # 100 years
        else:
            try:
                request.POST['expiration'] = float(request.POST['expiration'])
            except ValueError:
                request.POST['expiration'] = timedelta(days=36500)
            else:
                # 0 < 0.1 <= 360000
                if request.POST['expiration'] >= 360000:
                    request.POST['expiration'] = timedelta(days=360000)  # 1,000 years
                elif request.POST['expiration'] < 0:
                    raise HTTPBadRequest
                else:
                    request.POST['expiration'] = timedelta(days=request.POST['expiration'])

        if request.POST['user']:
            paste = UserPaste
        else:
            paste = Paste

        # Paste(paste, identifier=None, burn=False, expiration_delta=None, encryption=True, encryption_key=None)
        try:
            with manager:
                paste = paste(
                    paste=request.POST['content'],
                    expiration_delta=request.POST['expiration'],
                    encryption=request.POST['encryption'],
                    encryption_key=request.POST['key'],
                    burn=request.POST['burn'],
                )
                if request.POST['user']:
                    paste.user = request.POST['user']
                r = {
                    'encryption_key': paste.encryption_key,
                    'identifier': paste.identifier,
                }
                try:
                    DBSession.add(paste)
                except Timeout as e:
                    return Response(
                        str(e) + '\nPlease contact an administrator if the problem persists.',
                        content_type='text/plain',
                        status_int=500,
                    )
                DBSession.flush()
                deletion_token = paste.deletion_token
                regulator.update()
                DBSession.add(regulator)
        except OperationalError:
            logger = logging.getLogger(__name__)
            logger.exception(format_exc())
            raise HTTPServerError
        flash_response(
            request,
            'Your paste has been created <a href="{0}{1}">here</a>. '
            '<span class="right">[<a href="{0}{2}">Deletion link</a>.]</span>'.format(
                request.application_url,
                request.route_path(
                    'view_paste',
                    user=request.POST['user'] and request.POST['user'] + "/" or "",
                    id=r['identifier'],
                    key=r['encryption_key'] and "!" + r['encryption_key'] or "",
                    as_raw='',
                    to_remove='',
                ),
                request.route_path(
                    'view_paste',
                    user=request.POST['user'] and request.POST['user'] + "/" or "",
                    id=r['identifier'],
                    key='',
                    as_raw='',
                    to_remove="/remove/" + deletion_token,
                ),
            ),
            2,
            True,
        )
        return HTTPSeeOther(location=request.route_path('home') + '/')
    return {'content': ''}


@view_config(route_name='view_paste', renderer='view.mako')
def view_paste(request):
    # If the any information given is wrong, we increase the time anyway. To don't show which information is wrong.
    failed = DBSession.query(DecryptionAttempt).filter_by(address=request.remote_addr).first()
    if not failed:
        failed = DecryptionAttempt(address=request.remote_addr)
    elif failed.time >= 0:
        t = (datetime.utcnow() - failed.last_failure).seconds
        if t < failed.time * 40:  # = 5 attempt each 20s
            if failed.time > 10:
                raise HTTPForbidden(
                    'Slowdown!'
                    'If the key of the paste is wrong: do not force on it! Please wait about 3 minutes.'
                )
            sleep(failed.time if failed.time > -1 else 0)
        else:
            failed.decrement(failed.time * (t / 100))
            # if user tried five times and not tried after 20s we remove 0.17s (0.5*(20/60.0) = 0.1667).
    else:
        failed.time = 0

    raw = request.matchdict.get('as_raw')
    user = request.matchdict.get('USER')
    paste_id = request.matchdict.get('id')
    remove = request.matchdict.get('REMOVAL_KEY')

    def error(message=decryption_error_msg):
        with manager:
            failed.increment()
            DBSession.add(failed)
        return Response(message, content_type='text/plain', status_int=403) if raw else dict(message=message)

    if user:
        paste = DBSession.query(UserPaste).filter_by(user=user).filter_by(identifier=paste_id).first()
    else:
        paste = DBSession.query(Paste).filter_by(identifier=paste_id).first()
    if not paste:
        return error()

    # we check if the paste is expired or not.
    ti = 0
    tf = 0
    if paste.expire_date:
        ti = datetime.utcnow()
        tf = paste.expire_date
        if tf <= ti:  # if yes, we delete the paste and we return a response.
            DBSession.delete(paste)
            return error()

    # we check if user want to remove the paste.
    if remove:
        if paste.deletion_token == remove:
            DBSession.delete(paste)
            return error('The paste has been deleted.')
        return error('The paste can not be delete. Please check the deletion key.')

    # we check if the paste must be burned after reading. If yes, we remove it before displaying.
    if paste.instant_burn:
        DBSession.delete(paste)

    # if paste is encrypted, we check if the user has given a decryption key and we try to decrypt it.
    if paste.encrypted:
        key = request.matchdict.get('DECRYPTION_KEY')
        if key:
            try:
                r = {'paste': AESCipher(key).decrypt(paste.paste)}
            except ValueError:
                return error()
        else:
            return error()
    else:
        r = {'paste': paste.paste}

    # we can't reset the time, else each attempt in the case of brute force for example,
    # attacker just need to load a good one.
    DBSession.add(failed)

    if raw:
        return Response(r['paste'], content_type='text/plain', status_int=200)
    if paste.instant_burn:
        r['expiration_delta'] = 'This paste has been removed and ' \
                                'will never be showed again as a result of your reading.'
    else:
        if ti:
            r['expiration_delta'] = tf - ti
        else:
            r['expiration_delta'] = 'Unknown remaining time before the paste expiration. ' \
                                    'It is a "never, never" expiration (not maybe). Good job!'
    return r

decryption_error_msg = 'Sorry, this paste does not exist or we are unable to decrypt. ' \
                       'Please check the given information.'

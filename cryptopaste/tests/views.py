# ==== CryptoPaste
# AUTHOR: NyanKiyoshi
# COPYRIGHT: 2015 - NyanKiyoshi
# URL: https://github.com/NyanKiyoshi/CryptoPaste/
# LICENSE: https://github.com/NyanKiyoshi/CryptoPaste/master/LICENSE
#
# This file is part of CryptoPaste under the MIT license. Please take awareness about this latest before doing anything!

from cryptopaste.tests import *
from cryptopaste import views
from pyramid.httpexceptions import HTTPSeeOther


class TestPublicViews(BaseTest):
    def test_home(self):
        request = DummyRequest()
        response = views.home(request)
        self.assertIsInstance(response, dict)

    def test_invalid_link(self):
        request = DummyRequest(client_addr='127.0.0.1')
        request.matchdict['user'] = '_'
        response = views.view_paste(request)
        self.assertIn('message', response)

    def test_post(self):
        request = DummyRequest(
            post={
                'user': 'test',
                'content': 'One day, I would have wings.',
                'key': 'wings',
            },
            client_addr='127.0.0.1',
        )
        response = views.home(request)
        self.assertIsInstance(response, HTTPSeeOther)
        self.assertIn('_f_', request.session)
        r = request.session['_f_'][0][1]

        start, end = r.find('<a href="'), r.find('">')
        self.assertGreater(start, -1)
        self.assertGreater(end, -1)
        _id = r[start + 9:end].strip().split('/')[-1]

        start, end = r.find('[<a href="'), r.find('">Deletion link</a>')
        self.assertGreater(start, -1)
        self.assertGreater(end, -1)
        deletion_key = r[start + 10:end].strip().split('/')[-1]

        request = DummyRequest(client_addr='127.0.0.1')
        request.matchdict['USER'] = 'test'
        request.matchdict['id'] = _id
        request.matchdict['DECRYPTION_KEY'] = 'wings'
        request.matchdict['as_raw'] = True

        response = views.view_paste(request)
        self.assertEqual(response.body.decode('utf-8'), 'One day, I would have wings.')

        request.matchdict['as_raw'] = False
        response = views.view_paste(request)
        self.assertIn('paste', response)
        self.assertEqual(response['paste'], 'One day, I would have wings.')

        request.matchdict['as_raw'] = True
        request.matchdict['REMOVAL_KEY'] = deletion_key
        response = views.view_paste(request)
        self.assertEqual(response.body.decode('utf-8'), 'The paste has been deleted.')

        request.matchdict['REMOVAL_KEY'] = None
        self.assertEqual(views.view_paste(request).status_code, 403)

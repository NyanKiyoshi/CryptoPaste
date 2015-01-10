# -*- coding: utf-8 -*-
# ==== CryptoPaste
# AUTHOR: NyanKiyoshi
# COPYRIGHT: 2015 - NyanKiyoshi
# URL: https://github.com/NyanKiyoshi/CryptoPaste/
# LICENSE: https://github.com/NyanKiyoshi/CryptoPaste/master/LICENSE
#
# This file is part of CryptoPaste under the MIT license. Please take awareness about this latest before doing anything!

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config
from .models import DBSession, Base


def route(config, name, pattern, **kw):
    config.add_route(name, pattern, **kw)
    if not pattern.endswith('/'):
        config.add_route(name + '_', pattern + '/')

        def forwarder(request):
            return HTTPMovedPermanently(request.route_url(name, _query=request.GET, **request.matchdict))
        config.add_view(forwarder, route_name=name + '_')


def add_routes(config):
    route(config, 'home', '/')
    route(
        config,
        'view_paste',
        r'/'
        r'{user:((?P<USER>[a-zA-Z0-9]{1,80})/)?}'
        r'{id:[a-zA-Z0-9_\-.]{1,128}}'
        r'{key:(!(?P<DECRYPTION_KEY>[a-zA-Z0-9\-._]{1,600}))?}'
        r'{to_remove:(/remove/(?P<REMOVAL_KEY>[a-zA-Z0-9\-._]{100,400}))?}'
        r'{as_raw:(//raw)?}'
    )


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.set_session_factory(session_factory_from_settings(settings))
    add_routes(config)
    config.scan()
    return config.make_wsgi_app()

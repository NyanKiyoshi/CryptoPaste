# ==== CryptoPaste
# AUTHOR: NyanKiyoshi
# COPYRIGHT: 2015 - NyanKiyoshi
# URL: https://github.com/NyanKiyoshi/CryptoPaste/
# LICENSE: https://github.com/NyanKiyoshi/CryptoPaste/master/LICENSE
#
# This file is part of CryptoPaste under the MIT license. Please take awareness about this latest before doing anything!

from pyramid import testing
from sqlalchemy import engine_from_config
from paste.deploy.loadwsgi import appconfig
from cryptopaste.models import DBSession, Base
from cryptopaste import add_routes
import unittest
import os
from pyramid_beaker import session_factory_from_settings


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = appconfig('config:' + os.path.join(os.path.dirname(__file__), '../../', 'tests.ini'))
        cls.engine = engine_from_config(cls.settings, 'sqlalchemy.')

    def setUp(self):
        if 'mako.directories' not in self.settings:
            self.settings['mako.directories'] = 'ccvpn:templates/'
        if 'mako.imports' not in self.settings:
            self.settings['mako.imports'] = 'from ccvpn.filters import check'

        self.config = testing.setUp(settings=self.settings)
        self.config.include('pyramid_mako')
        self.config.include('pyramid_beaker')
        self.config.set_session_factory(session_factory_from_settings(self.settings))
        add_routes(self.config)

        DBSession.remove()

        self.connection = self.engine.connect()
        self.trans = self.connection.begin()

        DBSession.configure(bind=self.connection)
        Base.metadata.create_all(self.engine)
        self.session = DBSession

    def tearDown(self):
        testing.tearDown()
        self.trans.rollback()
        self.session.remove()
        self.connection.close()


class DummyRequest(testing.DummyRequest):
    def __init__(self, *args, **kwargs):
        super(DummyRequest, self).__init__(*args, **kwargs)
        self.referrer = None
        self.remote_addr = kwargs.get('remote_addr')


from cryptopaste.tests.models import *
from cryptopaste.tests.views import *
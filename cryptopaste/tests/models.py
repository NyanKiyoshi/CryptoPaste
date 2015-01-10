# ==== CryptoPaste
# AUTHOR: NyanKiyoshi
# COPYRIGHT: 2015 - NyanKiyoshi
# URL: https://github.com/NyanKiyoshi/CryptoPaste/
# LICENSE: https://github.com/NyanKiyoshi/CryptoPaste/master/LICENSE
#
# This file is part of CryptoPaste under the MIT license. Please take awareness about this latest before doing anything!

from cryptopaste.tests import *
from cryptopaste.models import Paste, UserPaste
from cryptopaste.utils import AESCipher


class TestUserModelWithDB(BaseTest):
    def setUp(self):
        super(TestUserModelWithDB, self).setUp()

        u = Paste(
            paste='Test.',
            burn=True,
            encryption=True,
        )
        self.identifier = u.identifier
        self.encryption_key = u.encryption_key

        self.session.add(u)
        self.session.flush()

    def test_results(self):
        p = self.session.query(Paste).filter_by(identifier=self.identifier).first()
        self.assertEqual(p.instant_burn, True)
        self.assertEqual(p.encrypted, True)
        self.assertEqual(AESCipher(self.encryption_key).decrypt(p.paste), "Test.")

    def test__(self):
        for action in [
            {
                'paste': 'Hello world?',
                'identifier': '0',
                'burn': False,
                'encryption': False,
                'encryption_key': None,
            },
            {
                'paste': 'Hello world!',
                'identifier': 'ident',
                'burn': True,
                'encryption': True,
                'encryption_key': 'Hey',
            },
        ]:
            self.session.add(
                Paste(
                    paste=action['paste'],
                    identifier=action['identifier'],
                    burn=action['burn'],
                    encryption=action['encryption'],
                    encryption_key=action['encryption_key'],
                )
            )
            self.session.flush()
            p = self.session.query(Paste).filter_by(identifier=action['identifier']).first()
            self.assertEqual(p.instant_burn, action['burn'])
            self.assertEqual(p.encrypted, action['encryption'])
            self.assertEqual(
                AESCipher(action['encryption_key']).decrypt(p.paste) if action['encryption']
                else p.paste, action['paste']
            )
        i = 0
        while 1:
            i += 1
            u = UserPaste(
                paste='Test.',
                burn=True,
                encryption=True,
            )
            self.identifier = u.identifier
            self.encryption_key = u.encryption_key
            u.user = 'New'

            DBSession.add(u)
            self.session.flush()
            p = self.session.query(UserPaste).filter_by(identifier=self.identifier).first()
            print '%s::Works fine.' % i
            self.assertEqual(p.instant_burn, True)
            self.assertEqual(p.encrypted, True)
            self.assertEqual(AESCipher(self.encryption_key).decrypt(p.paste), "Test.")
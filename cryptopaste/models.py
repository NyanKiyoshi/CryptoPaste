# ==== CryptoPaste
# AUTHOR: NyanKiyoshi
# COPYRIGHT: 2015 - NyanKiyoshi
# URL: https://github.com/NyanKiyoshi/CryptoPaste/
# LICENSE: https://github.com/NyanKiyoshi/CryptoPaste/master/LICENSE
#
# This file is part of CryptoPaste under the MIT license. Please take awareness about this latest before doing anything!

from sqlalchemy import Boolean, Column, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from datetime import datetime, timedelta
from cryptopaste.utils import AESCipher, new_key

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(keep_session=False)))
Base = declarative_base()


class Timeout(Exception):
    pass


class Paste(Base):
    __tablename__ = 'pastes'
    id = Column(Integer, primary_key=True, nullable=False)
    identifier = Column(String, nullable=False, unique=True)
    paste = Column(Text, nullable=False)
    encrypted = Column(Boolean, nullable=False, default=True)
    expire_date = Column(DateTime, nullable=True, default=None)
    year_month = Column(String(4), nullable=False)
    instant_burn = Column(Boolean, nullable=False, default=False)
    deletion_token = Column(String(700), nullable=False, default=new_key(min_length=100, max_length=400))

    def __init__(self, paste, identifier=None, burn=False, expiration_delta=None, encryption=True, encryption_key=None):
        """
        :param paste:
        :type paste str:
            The paste's content (encrypted or not, according `encrypted`).
        :param expiration_delta:
        :type expiration_delta timedelta:
            About 100 years by default.
        :param encryption:
        :type encryption bool:
            If the `paste` must be encrypted or not.
        :param encryption_key:
        :type encryption_key str:
            Sets manually an encryption key instead of the random key (unrecommended).
        :return:
        """
        now = datetime.utcnow()
        d = [str(now.year)[2:], str(now.day)]
        self.year_month = d[0] + d[1]

        if burn:
            self.instant_burn = True
        else:
            self.expire_date = now + (
                expiration_delta if type(expiration_delta) is timedelta else timedelta(days=365 * 100)
            )

        if encryption:
            if not encryption_key:
                self.encryption_key = new_key(min_length=90, max_length=600)
            else:
                self.encryption_key = encryption_key
            self.paste = AESCipher(self.encryption_key).encrypt(paste.encode('utf-8'))
        else:
            self.paste = paste
            self.encrypted = False
            self.encryption_key = None

        n = DBSession.query(Paste).filter_by(year_month=self.year_month).count()
        # 74 possibilities * len for the identifier
        # 5250 possibilities for the decryption key
        n = int((n / 74) + 1)
        self.identifier = identifier if identifier else new_key(
            begin=d[0], end=d[1], length=n+2, min_length=n, chars='a-zA-Z0-9_-.'
        )
        i = [0, 0]
        q = DBSession.query(Paste).filter_by(identifier=self.identifier).first()
        while q:
            self.identifier = new_key(begin=d[0], end=d[1], length=n+2, min_length=n, chars='a-zA-Z0-9_-.')
            q = DBSession.query(Paste).filter_by(identifier=self.identifier).first()
            i[0] += 1
            if i[0] == 15:
                n += 2
                i[1] += i[0]
                i[0] = 0
            if i[1] == 100:
                raise Timeout('The identifier creation exceeded the limit...')


class UserPaste(Base):
    __tablename__ = 'users_pastes'
    id = Column(Integer, primary_key=True)
    user = Column(String(80), nullable=True)
    identifier = Column(String, nullable=False, unique=True)
    paste = Column(Text, nullable=False)
    encrypted = Column(Boolean, nullable=False, default=True)
    expire_date = Column(DateTime, nullable=True, default=None)
    year_month = Column(String(4), nullable=False)
    instant_burn = Column(Boolean, nullable=False, default=False)
    deletion_token = Column(String(700), nullable=False, default=new_key(min_length=250, max_length=400))

    def __init__(self, paste, identifier=None, burn=False, expiration_delta=None, encryption=True, encryption_key=None):
        """
        :param paste:
        :type paste str:
            The paste's content (encrypted or not, according `encrypted`).
        :param expiration_delta:
        :type expiration_delta timedelta:
            About 100 years by default.
        :param encryption:
        :type encryption bool:
            If the `paste` must be encrypted or not.
        :param encryption_key:
        :type encryption_key str:
            Sets manually an encryption key instead of the random key (unrecommended).
        :return:
        """
        now = datetime.utcnow()
        d = [str(now.year)[2:], str(now.day)]
        self.year_month = d[0] + d[1]

        if burn:
            self.instant_burn = True
        else:
            self.expire_date = now + (
                expiration_delta if type(expiration_delta) is timedelta else timedelta(days=365 * 100)
            )

        if encryption:
            if not encryption_key:
                self.encryption_key = new_key(min_length=90, max_length=600)
            else:
                self.encryption_key = encryption_key
            self.paste = AESCipher(self.encryption_key).encrypt(paste.encode('utf-8'))
        else:
            self.paste = paste
            self.encrypted = False
            self.encryption_key = None

        n = DBSession.query(UserPaste).filter_by(year_month=self.year_month).count()
        # 74 possibilities * len for the identifier
        # 5250 possibilities for the decryption key
        n = int((n / 74) + 1)
        self.identifier = identifier if identifier else new_key(
            begin=d[0], end=d[1], length=n+2, min_length=n, chars='a-zA-Z0-9_-.'
        )
        i = [0, 0]
        q = DBSession.query(UserPaste).filter_by(identifier=self.identifier).first()
        while q:
            self.identifier = new_key(begin=d[0], end=d[1], length=n+2, min_length=n, chars='a-zA-Z0-9_-.')
            q = DBSession.query(UserPaste).filter_by(identifier=self.identifier).first()
            i[0] += 1
            if i[0] == 15:
                n += 2
                i[1] += i[0]
                i[0] = 0
            if i[1] == 100:
                raise Timeout('The identifier creation exceeded the limit...')


class DecryptionAttempt(Base):
    __tablename__ = 'decryption_attempts'
    id = Column(Integer, primary_key=True)
    time = Column(Float, nullable=False, default=0.0)
    last_failure = Column(DateTime, nullable=False, default=datetime.utcnow())
    address = Column(String(50), nullable=False, unique=True)

    def __init__(self, address, time=0.0):
        self.address = address
        self.time = time

    def increment(self, of=0.10):
        self.time += of
        self.last_failure = datetime.utcnow()

    def decrement(self, of=0.02):
        if self.time < of:
            self.time = 0
        else:
            self.time -= of

    def reset(self):
        self.time = 0.0


class SubmissionRegulator(Base):
    __tablename__ = 'submissions_regulator'
    id = Column(Integer, primary_key=True)
    next_time = Column(DateTime, nullable=False, default=datetime.utcnow() + timedelta(seconds=30))
    address = Column(String(50), nullable=False, unique=True)

    def update(self):
        self.next_time = datetime.utcnow() + timedelta(seconds=30)

Index(Paste, Paste.identifier)
Index(UserPaste, UserPaste.user, UserPaste.identifier)

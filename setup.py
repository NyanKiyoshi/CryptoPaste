import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'mako',
    'pyramid_mako',
    'pyramid_beaker',
    'pycrypto',
    # POSIX:
    # If you receive "error: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 1":
    #       Try to install python3-dev for Python3 or python-dev for Python2 on Debian or python-devel for yum package
    #       manager. (Not needed on ArchLinux).
    #
    # Windows:
    # If `pycrypto` doesn't compile and your are on Windows, before call setup.py,
    #    you must have VisualStudio installed and you need to run one of these according of your VS version:
    #           VS10 (2011) => SET VS90COMNTOOLS=%VS100COMNTOOLS%
    #           VS11 (2012) => SET VS90COMNTOOLS=%VS110COMNTOOLS%
    #           VS12 (2013) => SET VS90COMNTOOLS=%VS120COMNTOOLS%
    # [Source: http://stackoverflow.com/a/10558328]
    #
    # If it does not work you can also run:
    #   For Python3.3+:
    #   32bits:
    #   .\env\Scripts\easy_install.exe http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py3.3.exe
    #   64 bits:
    #   .\env\Scripts\easy_install.exe http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py3.3.exe
    #   Or for Python2.6+:
    #   32bits:
    #   .\env\Scripts\easy_install.exe http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py3.2.exe
    #   64bits:
    #   .\env\Scripts\easy_install.exe http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py3.2.exe
]

setup(
    name='CryptoPaste',
    version='0.1.3',
    description='CryptoPaste',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web WSGI bfg pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='cryptopaste',
    install_requires=requires,
    entry_points="""\
        [paste.app_factory]
        main = cryptopaste:main
        [console_scripts]
        init_db = cryptopaste.init_db:main
    """,
)

CryptoPaste
===========
Encrypt and decrypt easily your texts and make them available for the entire world by the way of a link.

Requirements
============
Python (at least 2.6 or 3.3).

Getting Started (for POSIX user)
================================
1. Clone the project and change dir into.
```bash
git clone https://github.com/NyanKiyoshi/cryptopaste.git && cd cryptopaste
```
2. Create the Python virtual environment.
```bash
virtualenv-2.7 --python /usr/bin/python2 --no-site-packages env
```
3. Install the requirements and the project.
```bash
./env/bin/python setup.py develop
```
4. Initialize the database.
```bash
./env/bin/init_db development.ini
```

Run the server
==============
```bash
./env/bin/pserve development.ini
```

CryptoPaste
===========
Encrypt and decrypt easily your texts and make them available for the entire world by the way of a link.

Index
=====
1. [Requirements](#requirements)
2. [Getting Started (for POSIX user)](#getting-started-for-posix-user)
3. [Run the server](#run-the-server)
4. [Full documentation](#full-documentation)
5. [Troubleshooting](#troubleshooting)
6. [Troubleshooting](#how-to-contribute)

Requirements
============
Python (at least 2.6 or 3.3). Python2.x is recommended for this project.

Getting Started (for POSIX user)
================================
1\. Clone the project and change dir into.
```bash
git clone https://github.com/NyanKiyoshi/cryptopaste.git && cd cryptopaste
```
2\. Create the Python virtual environment.
```bash
virtualenv-2.7 --python /usr/bin/python2 --no-site-packages env
```
3\. Install the requirements and the project.
```bash
./env/bin/python setup.py develop
```
4\. Initialize the database.
```bash
./env/bin/init_db development.ini
```

Run the server
==============
```bash
./env/bin/pserve development.ini
```

Full documentation
==================
You can find more information about this project [here](http://nyankiyoshi.github.io/docs/CryptoPaste/0.1/index.html)

Troubleshooting
===============
You have a problem? Or an issue?

You can try to find an answer to you problem [here](http://nyankiyoshi.github.io/docs/CryptoPaste/0.1/troubleshooting.html).
If you can't find the good answer for your problem, feel free to post [here](https://github.com/NyanKiyoshi/CryptoPaste/issues).

How to contribute?
==================
Report issues, submit [pull requests](https://github.com/NyanKiyoshi/CryptoPaste/pulls) to fix problems (or possible problems), improvements, ideas, etc.

Feel free to contribute to this project like you want and don't be shy!

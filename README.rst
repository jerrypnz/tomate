===========
Tomate
===========


1. Introduction
===============
Tomate is a time management tool inspired by the pomodoro technique.


2. Installation
===============
You need the following packages to install tomate:

1. setuptools (http://pypi.python.org/pypi/setuptools)
2. distutils-extra (https://launchpad.net/python-distutils-extra)

Tomate needs the following python packages to run:

1. PyGTK
2. PyNotify
3. PyCairo

Please install these packages before you install Tomate.
It is recommended to install these packages through your distro's package
manager. For Ubuntu, use the following commands to install them::

    sudo apt-get install python-setuptools
    sudo apt-get install python-pip
    sudo apt-get install python-distutils-extra
    sudo apt-get install python-gtk2
    sudo apt-get install python-notify
    sudo apt-get install python-cairo

Use the following command to install Tomate::
    
    sudo python setup.py install --root=/

For Ubuntu users, please add --install-layout=deb option, like this::

    sudo python setup.py install --root=/ --install-layout=deb


3. License
===========
This program is released under the GNU General Public License (GPL) version 3, read
'COPYING' for more information.


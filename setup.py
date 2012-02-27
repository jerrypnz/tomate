#!/usr/bin/env python

from setuptools import setup
from tomate import __version__

setup(
    name='tomate',
    version=__version__,
    description='Tomate is a tool for pomodoro technique, powered by PyGTK',
    author='Jerry Peng',
    author_email='pr2jerry@gmail.com',
    url='https://github.com/moonranger/tomate',
    packages=['tomate'],
    requires=['pygtk(>=2.4)', 'pynotify'],
    entry_points = {
        'gui_scripts': ['tomate=tomate.ui:start_app'],
        },
    data_files = [
        ('share/applications', ['data/tomate.desktop']),
        ],
    license='GNU GPL v3',
    platforms='linux'
)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Jerry Peng
#
# Tomate is a time management tool inspired by the
# pomodoro technique(http://www.pomodorotechnique.com/).
#
# Tomate is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option
# any later version.
#
# Tomate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with Foobar. If not, see http://www.gnu.org/licenses/.


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


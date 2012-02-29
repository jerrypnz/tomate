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


import os.path
import os

class Config(object):
    """Configuration object"""
    def __init__(self):
        super(Config, self).__init__()
        self.conf_dir = os.path.expanduser('~/.tomate/')
        self.db_file = 'data.db'
        self._create_conf_dir()

    def _create_conf_dir(self):
        if os.path.isdir(self.conf_dir):
            return
        if os.path.exists(self.conf_dir):
            os.unlink(self.conf_dir)
        os.mkdir(self.conf_dir)

    def get_db_filename(self):
        return os.path.join(self.conf_dir, self.db_file)

conf = Config()


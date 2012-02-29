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


import pygtk
pygtk.require('2.0')
import gtk

import logging
import pynotify

pynotify.init("PyTomato")

def show_notification(title, msg):
    """show a notification message"""
    n = pynotify.Notification(title, msg, 'stock_view-details')
    n.show()


def new_text_col(colname, data_func):
    renderer = gtk.CellRendererText()
    col = gtk.TreeViewColumn(colname, renderer)
    col.set_cell_data_func(renderer, data_func)
    return col


def new_small_button(iconname, click_callback, tooltip=None, relief=gtk.RELIEF_NONE):
    btn = gtk.Button()
    btn.set_image(gtk.image_new_from_icon_name(iconname, gtk.ICON_SIZE_BUTTON))
    if tooltip:
        btn.set_tooltip_text(tooltip)
    btn.set_focus_on_click(False)
    btn.set_relief(relief)
    btn.connect('clicked', click_callback)
    return btn


def show_message_dialog(msg, type=gtk.MESSAGE_INFO):
    main_window = globals().get('main_window', None)
    msg_dialog = gtk.MessageDialog(parent=main_window, type=type, buttons=gtk.BUTTONS_OK, message_format=msg)
    msg_dialog.run()
    msg_dialog.destroy()


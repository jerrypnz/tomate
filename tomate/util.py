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


def show_message_dialog(msg, type=gtk.MESSAGE_INFO):
    main_window = globals().get('main_window', None)
    msg_dialog = gtk.MessageDialog(parent=main_window, type=type, buttons=gtk.BUTTONS_OK, message_format=msg)
    msg_dialog.run()
    msg_dialog.destroy()


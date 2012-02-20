import pygtk
pygtk.require('2.0')
import gtk


class HistoryView(gtk.Label):
    """docstring for HistoryView"""
    def __init__(self, parent_window):
        super(HistoryView, self).__init__('History View')


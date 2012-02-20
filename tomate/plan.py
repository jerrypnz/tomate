import pygtk
pygtk.require('2.0')
import gtk


class PlanView(gtk.Label):
    """docstring for PlanView"""
    def __init__(self, parent_window):
        super(PlanView, self).__init__('Plan View')


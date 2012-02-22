import pygtk
pygtk.require('2.0')
import gtk

from datetime import date
from tomate.uimodel import FinishedTomatoModel

class HistoryView(gtk.HPaned):
    """Activity history view"""
    def __init__(self, parent_window):
        super(HistoryView, self).__init__()
        self.parent_window = parent_window
        self.calendar = gtk.Calendar()
        self.tomato_view = self._create_tomato_view()
        self.tomato_model = self.tomato_view.get_model()
        self.act_view = self._create_activity_view()
        self.act_model = self.act_view.get_model()

        act_wnd = gtk.ScrolledWindow()
        act_wnd.add(self.act_view)
        act_wnd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        tomato_wnd = gtk.ScrolledWindow()
        tomato_wnd.add(self.tomato_view)
        tomato_wnd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        top_box = gtk.VBox(False, 2)
        top_box.pack_start(self.calendar, False, False)
        top_box.pack_end(act_wnd, True, True)

        self.pack1(top_box, shrink=False)
        self.pack2(tomato_wnd, shrink=False)

        self._on_day_changed(self.calendar)
        self.calendar.connect('day-selected', self._on_day_changed)

    def _create_tomato_view(self):
        def _set_bg(col, renderer, model, iter, user_data=None):
            interrupted = model.get_value(iter, 2)
            bgcolor = interrupted and '#F79292' or '#92F792'
            renderer.set_property('cell-background', bgcolor)

        view = gtk.TreeView()
        model = FinishedTomatoModel()
        view.set_model(model)
        time_renderer = gtk.CellRendererText()
        time_col = gtk.TreeViewColumn('Time Range', time_renderer, text=0)
        time_col.set_cell_data_func(time_renderer, _set_bg)
        time_col.set_resizable(True)
        time_col.set_expand(True)

        activity_renderer = gtk.CellRendererText()
        activity_col = gtk.TreeViewColumn('Activity', activity_renderer, text=1)
        activity_col.set_cell_data_func(activity_renderer, _set_bg)
        activity_col.set_resizable(True)
        activity_col.set_expand(True)
        view.append_column(time_col)
        view.append_column(activity_col)
        return view

    def _create_activity_view(self):
        view = gtk.TreeView()
        model = gtk.ListStore(bool, str)
        view.set_model(model)
        finish_col = gtk.TreeViewColumn('#', gtk.CellRendererToggle(), active=0)
        activity_col = gtk.TreeViewColumn('Finished Activity', gtk.CellRendererText(), text=1)
        view.append_column(finish_col)
        view.append_column(activity_col)
        model.append((True, 'Play football'))
        model.append((True, 'Write program'))
        return view

    def _on_day_changed(self, calendar):
        y, m, d = calendar.get_date()
        #The month is 0-based, so we need to add 1 to it
        selected_day = date(y, m + 1, d)
        self.tomato_model.load_finished_tomatoes(selected_day)


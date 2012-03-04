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

from datetime import date
from tomate.uimodel import FinishedTomatoModel, FinishedActivityModel

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
        self.statistics = gtk.Label()
        self.statistics.set_justify(gtk.JUSTIFY_RIGHT)

        act_wnd = gtk.ScrolledWindow()
        act_wnd.add(self.act_view)
        act_wnd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        act_wnd.set_size_request(-1, 130)

        tomato_wnd = gtk.ScrolledWindow()
        tomato_wnd.add(self.tomato_view)
        tomato_wnd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        pane = gtk.VPaned()
        pane.pack1(act_wnd, shrink=False)
        pane.pack2(tomato_wnd, shrink=False)

        box1 = gtk.VBox(False, 0)
        box1.pack_start(self.calendar, False, False, padding=5)
        box1.pack_start(self.statistics, False, False, padding=15)

        box2 = gtk.HBox(False, 0)
        box2.pack_start(box1, True, True, padding=5)

        self.pack1(box2, shrink=False)
        self.pack2(pane, shrink=False)

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
        time_col = gtk.TreeViewColumn(_('Time Range'), time_renderer, text=0)
        time_col.set_cell_data_func(time_renderer, _set_bg)
        time_col.set_resizable(True)
        time_col.set_expand(True)

        activity_renderer = gtk.CellRendererText()
        activity_col = gtk.TreeViewColumn(_('Activity'), activity_renderer, text=1)
        activity_col.set_cell_data_func(activity_renderer, _set_bg)
        activity_col.set_resizable(True)
        activity_col.set_expand(True)
        view.append_column(time_col)
        view.append_column(activity_col)
        return view

    def _create_activity_view(self):
        view = gtk.TreeView()
        model = FinishedActivityModel()
        view.set_model(model)
        finish_col = gtk.TreeViewColumn('#', gtk.CellRendererToggle(), active=0)
        activity_col = gtk.TreeViewColumn(_('Finished Activity'), gtk.CellRendererText(), text=1)
        view.append_column(finish_col)
        view.append_column(activity_col)
        return view

    def refresh(self):
        self._on_day_changed(self.calendar)

    def _on_day_changed(self, calendar):
        y, m, d = calendar.get_date()
        #The month is 0-based, so we need to add 1 to it
        selected_day = date(y, m + 1, d)
        tomato_count, interruption_count = self.tomato_model.load_finished_tomatoes(selected_day)
        finished_act_count = self.act_model.load_finished_activities(selected_day)
        markup = '''
        <span foreground="#32CD32">%s: %-s</span>
        <span foreground="#CD3232">%s: %-s</span>
        %s: %-s''' % (
            _('Tomatoes'), tomato_count,
            _('Interruptions'), interruption_count,
            _('Finished Activities'), finished_act_count,
            )
        self.statistics.set_markup(markup)


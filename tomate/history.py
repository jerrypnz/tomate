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
from tomate.uimodel import FinishedTomatoModel
from tomate.uimodel import FinishedActivityModel
from tomate.uimodel import WeeklyStatisticsModel
from tomate.chart import WeeklyBarChart

class HistoryView(gtk.VPaned):
    """Activity history view"""
    def __init__(self, parent_window):
        super(HistoryView, self).__init__()
        self.parent_window = parent_window
        self.calendar = gtk.Calendar()
        self.tomato_view = self._create_tomato_view()
        self.tomato_model = self.tomato_view.get_model()
        self.stat_model = WeeklyStatisticsModel()
        self.stat_graph = WeeklyBarChart(self.stat_model)

        tomato_wnd = gtk.ScrolledWindow()
        tomato_wnd.add(self.tomato_view)
        tomato_wnd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        box1 = gtk.VBox(False, 0)
        box1.pack_start(self.calendar, True, False, padding=5)

        box2 = gtk.HBox(False, 0)
        box2.pack_start(box1, True, False, padding=5)

        box3 = gtk.VBox(False, 0)
        box3.pack_start(tomato_wnd, True, True, padding=5)

        pane = gtk.HPaned()
        pane.pack1(box2, shrink=False)
        pane.pack2(box3, shrink=False)

        self.pack1(pane, shrink=False)
        self.pack2(self.stat_graph, shrink=False)

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

    def refresh(self):
        self._on_day_changed(self.calendar)

    def _on_day_changed(self, calendar):
        y, m, d = calendar.get_date()
        #The month is 0-based, so we need to add 1 to it
        selected_day = date(y, m + 1, d)
        tomato_count, interruption_count = self.tomato_model.load_finished_tomatoes(selected_day)
        self.stat_model.reload_data(selected_day)


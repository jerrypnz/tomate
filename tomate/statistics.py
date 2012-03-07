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
import gobject
from datetime import datetime, date, timedelta, time

from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

from tomate import model

TABS = [
        (_('Week'),         'WeekView'),
        (_('Month'),        'MonthView'),
        (_('Advanced'),     'AdvancedView'),
        ]

class StatisticsView(gtk.VBox):
    """Statistics View"""
    def __init__(self, parent_window):
        super(StatisticsView, self).__init__(False, 0)
        self.parent_window = parent_window
        self.store = model.open_store()
        self.connect('destroy', lambda arg : self.store.close())
        self.notebook = self._setup_tabs()
        padding = 2
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(self.notebook, True, True, padding=padding)
        self.pack_start(hbox, True, True, padding=padding)

    def _setup_tabs(self):
        notebook = gtk.Notebook()
        g = globals()
        for name, clsname in TABS:
            view = g[clsname](self.store)
            notebook.append_page(view, gtk.Label(name))
        return notebook

    def refresh(self):
        pass


class WeekView(FigureCanvas):
    """docstring for WeekView"""
    def __init__(self, store):
        today = date.today()
        weekday = today.weekday()
        start_day = today - timedelta(days=weekday)
        end_day = today + timedelta(days=6-weekday-1)
        start_time = datetime.combine(start_day, time(0, 0, 0))
        end_time = datetime.combine(end_day, time(23, 59, 59))
        f = self._generate_figure(store, start_time, end_time)
        super(WeekView, self).__init__(f)
        self.show()

    def _generate_figure(self, store, time1, time2):
        statistics = store.statistics_tomato_count(time1, time2)
        dates = [datetime.fromtimestamp(a[0]).date() for a in statistics]
        finish_counts = [a[1][0] for a in statistics]
        interrupt_counts = [a[1][1] for a in statistics]
        f = Figure(figsize=(6, 5), dpi=60)
        ax = f.add_subplot(111)
        width = 0.3
        tomato_legend = ax.bar(dates, finish_counts,
                width=width,
                color='#92F792',
                label=_('Tomatoes'))
        interrupt_legend = ax.bar(dates, interrupt_counts,
                bottom=finish_counts,
                width=width,
                color='#F79292',
                label=_('Interruptions'))
        ax.legend(loc=2)
        ax.set_xticks(dates)
        ax.set_xticklabels([d.strftime("%a") for d in dates], ha='right')
        ax.set_xlabel(_('Weekday'))
        ax.set_ylabel(_('Number of Tomatoes'))
        return f


class MonthView(gtk.Label):
    """docstring for MonthView"""
    def __init__(self, store):
        super(MonthView, self).__init__('Month View')


class AdvancedView(gtk.Label):
    """docstring for AdvancedView"""
    def __init__(self, store):
        super(AdvancedView, self).__init__('Advanced View')

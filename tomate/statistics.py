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
import cairo
import math

from datetime import datetime, date, timedelta, time

from tomate.uimodel import WeeklyStatisticsModel

class StatisticsView(gtk.VBox):
    """Statistics View"""
    def __init__(self, parent_window):
        super(StatisticsView, self).__init__(False, 0)
        self.parent_window = parent_window
        self.stat_model = WeeklyStatisticsModel()
        self.graph = WeeklyGraph(self.stat_model)
        padding = 1
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(self.graph, True, True, padding=padding)
        self.pack_start(hbox, True, True, padding=padding)

    def refresh(self):
        self.graph.refresh()


class WeeklyGraph(gtk.DrawingArea):

    __gsignals__ = { "expose-event": "override" }

    def __init__(self, model):
        super(WeeklyGraph, self).__init__()
        self.model = model
        self.set_size_request(500, 400)
        self.date = date.today()

    def select_day(self, date):
        self.date = date
        self.refresh()

    def refresh(self):
        self.model.reload_data(self.date)

    def do_expose_event(self, event):
        cr = self.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()
        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        renderer = BarGraphRenderer(cr, width, height, self.model.get_data())
        renderer.render()


class BarGraphRenderer(object):
    BG_COLOR = (0.9, 0.9, 0.9)
    BORDER_COLOR = (0.0, 0.0, 0.0)
    FG_COLOR = (1, 1, 1)
    V1_COLOR = (0.32, 0.75, 0.00)
    V2_COLOR = (0.89, 0.35, 0.16)
    TICK_LEN = 3
    LEGEND_WIDTH = 30
    LEGEND_HEIGHT = 13

    def __init__(self, ctx, width, height, data):
        super(BarGraphRenderer, self).__init__()
        self.ctx = ctx
        self.x_reserv = width / 20
        self.width = width
        self.height = height
        self.data = data

    def rad_gradient(self, color1, color2):
        radial = cairo.LinearGradient(0.0, 0.0, 0.0, self.graph_height)
        radial.add_color_stop_rgb(0, *color2)
        radial.add_color_stop_rgb(1, *color1)
        return radial

    def render(self):
        self._calculate()
        self.ctx.select_font_face('Sans')
        self.ctx.set_font_size(9)
        self._draw_background(self.ctx)
        self._draw_cordinates(self.ctx)
        self._draw_bars(self.ctx)
        self._draw_legends(self.ctx)

    def _calculate(self):
        self.border_width = 45
        self.graph_width = self.width - 2 * self.border_width
        self.graph_height = self.height - 2 * self.border_width
        self.x_max = len(self.data)
        self.y_max = max([max(d) for l, d in self.data]) + 2
        self.x_tick_span = (self.graph_width - self.x_reserv) / self.x_max + 2
        self.x_ticks = range(self.x_reserv, self.graph_width, self.x_tick_span)
        self.y_tick_span = self.graph_height / self.y_max + 2
        self.y_ticks = range(0, self.graph_height, self.y_tick_span)

    def _draw_background(self, cr):
        cr.set_source_rgb(*self.FG_COLOR)
        cr.rectangle(self.border_width,
                self.border_width,
                self.width - 2 * self.border_width,
                self.height - 2 * self.border_width)
        cr.fill_preserve()
        cr.set_line_width(0.4)
        cr.set_source_rgb(*self.BORDER_COLOR)
        cr.stroke()
        cr.translate(self.border_width, self.border_width)

    def _draw_cordinates(self, cr):
        cr.set_source_rgb(*self.BORDER_COLOR)
        for i, x_tick in enumerate(self.x_ticks):
            cr.move_to(x_tick, self.graph_height)
            cr.line_to(x_tick, self.graph_height - 2)
            cr.move_to(x_tick - self.TICK_LEN, self.graph_height + 10)
            cr.show_text(self.data[i][0])
        cr.move_to(self.graph_width / 2 - 30, self.graph_height + 30)
        cr.show_text('Weekdays')
        for i, y_tick in enumerate(self.y_ticks[1:], 1):
            cr.move_to(0, self.graph_height - y_tick)
            cr.line_to(self.TICK_LEN, self.graph_height - y_tick)
            cr.move_to(self.graph_width, self.graph_height - y_tick)
            cr.line_to(self.graph_width - 3, self.graph_height - y_tick)
            cr.move_to(-20, self.graph_height - y_tick)
            cr.show_text(str(i))
        cr.stroke()
        cr.move_to(-30, self.graph_height / 2 + 30)
        cr.save()
        text_matrix = cr.get_font_matrix()
        text_matrix.rotate(-math.pi * 0.5)
        cr.set_font_matrix(text_matrix)
        cr.show_text('Number of Tomatoes')
        cr.restore()

    def _draw_bars(self, cr):
        bar_width = self.x_tick_span / 4
        for i, (l, (v1, v2)) in enumerate(self.data):
            v1_bar_height = max(self.y_tick_span * v1, 1)
            v2_bar_height = max(self.y_tick_span * v2, 1)
            cr.set_source_rgb(*self.V1_COLOR)
            cr.rectangle(self.x_ticks[i] - bar_width,
                    self.graph_height - v1_bar_height,
                    bar_width,
                    v1_bar_height)
            cr.fill_preserve()
            cr.set_source_rgba(0.0, 0.0, 0.0, 0.5)
            cr.stroke()
            cr.set_source_rgb(*self.V2_COLOR)
            cr.rectangle(self.x_ticks[i],
                    self.graph_height - v2_bar_height,
                    bar_width,
                    v2_bar_height)
            cr.fill_preserve()
            cr.set_source_rgba(0.0, 0.0, 0.0, 0.5)
            cr.stroke()

    def _draw_legends(self, cr):
        cr.translate(0, 0)
        cr.rectangle(self.LEGEND_WIDTH,
                self.LEGEND_HEIGHT,
                self.LEGEND_WIDTH,
                self.LEGEND_HEIGHT)
        cr.set_source_rgb(*self.V1_COLOR)
        cr.fill_preserve()
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.5)
        cr.stroke()
        cr.rectangle(self.LEGEND_WIDTH,
                self.LEGEND_HEIGHT * 3,
                self.LEGEND_WIDTH,
                self.LEGEND_HEIGHT)
        cr.set_source_rgb(*self.V2_COLOR)
        cr.fill_preserve()
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.5)
        cr.stroke()
        cr.set_source_rgb(*self.BORDER_COLOR)
        cr.move_to(self.LEGEND_WIDTH * 2 + 10, self.LEGEND_HEIGHT + 10)
        cr.show_text('Finished')
        cr.move_to(self.LEGEND_WIDTH * 2 + 10, self.LEGEND_HEIGHT * 3 + 10)
        cr.show_text('Interrupted')


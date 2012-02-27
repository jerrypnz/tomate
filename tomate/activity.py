import pygtk
pygtk.require('2.0')
import gtk
import gobject

from tomate import model
from tomate import util
from tomate.uimodel import ActivityStore

class ActivityView(gtk.VBox):
    """Current todo activities view"""
    def __init__(self, parent_window):
        super(ActivityView, self).__init__(False, 3)
        self.parent_window = parent_window
        self.act_name = gtk.Entry()
        self.act_name.set_property('secondary-icon-stock', gtk.STOCK_ADD)
        self.act_name.set_property('secondary-icon-tooltip-text', 'Add new activity')
        self.act_name.set_property('secondary-icon-activatable', True)
        self.act_name.connect('activate', self._on_add)
        self.act_name.connect('icon-press', self._on_add)
        self.act_name.connect('focus-in-event', self._on_focus)

        self.start_button = gtk.Button()
        self.start_button.set_tooltip_text('Start a tomato timer and work on selected activity')
        self.start_button.set_image(gtk.image_new_from_icon_name(
                    'media-playback-start', gtk.ICON_SIZE_BUTTON))
        self.start_button.set_relief(gtk.RELIEF_NONE)
        self.start_button.connect('clicked', self._on_start_timer)

        self.finish_button = gtk.Button()
        self.finish_button.set_tooltip_text('Mark the selected activity as finished')
        self.finish_button.set_image(gtk.image_new_from_icon_name(
                    'dialog-ok', gtk.ICON_SIZE_BUTTON))
        self.finish_button.set_relief(gtk.RELIEF_NONE)
        self.finish_button.connect('clicked', self._on_mark_finish)

        self.delete_button = gtk.Button()
        self.delete_button.set_tooltip_text('Remove the selected activity')
        self.delete_button.set_image(gtk.image_new_from_icon_name(
                    'edit-delete', gtk.ICON_SIZE_BUTTON))
        self.delete_button.set_relief(gtk.RELIEF_NONE)
        self.delete_button.connect('clicked', self._on_del_activity)

        new_act_hbox = gtk.HBox(False, 4)
        new_act_hbox.pack_start(self.start_button, False, False)
        new_act_hbox.pack_start(self.finish_button, False, False)
        new_act_hbox.pack_start(self.delete_button, False, False)

        self.act_view = self._create_list_view()
        self.act_model = self.act_view.get_model()

        self.connect('destroy', lambda arg : self.act_model.close())

        act_wnd = gtk.ScrolledWindow()
        act_wnd.add(self.act_view)
        act_wnd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.pack_start(new_act_hbox, False, False)
        self.pack_start(act_wnd, True, True)
        self.pack_end(self.act_name, False, False)

    def _create_list_view(self):

        def _act_name_render_func(col, renderer, model, iter, user_data=None):
            name = model.get_value(iter, ActivityStore.TITLE_COL)
            finished = model.get_value(iter, ActivityStore.FINISHED_COL)
            if finished:
                name = '<span foreground="#32CD32"><s>%s</s></span>' % name
            renderer.set_property('markup', name)

        def _tomato_render_func(col, renderer, model, iter, user_data=None):
            tomatoes = model.get_value(iter, ActivityStore.TOMATO_COL)
            renderer.set_property('markup', '<span foreground="#32CD32">%s</span>' % tomatoes)

        def _interrupt_render_func(col, renderer, model, iter, user_data=None):
            interrupts = model.get_value(iter, ActivityStore.INTERRUPT_COL)
            renderer.set_property('markup', '<span foreground="#CD3232">%s</span>' % interrupts)

        act_model = ActivityStore()
        act_view = gtk.TreeView()
        act_view.set_model(act_model)

        toggle_renderer = gtk.CellRendererToggle()
        toggle_renderer.set_property('activatable', True)
        toggle_renderer.connect('toggled', self._on_toggle_finish)
        toggle_col = gtk.TreeViewColumn('#', toggle_renderer, active=1)
        toggle_col.set_expand(False)
        title_col = util.new_text_col('Activity', _act_name_render_func)
        title_col.set_resizable(True)
        title_col.set_expand(True)
        tomato_col = util.new_text_col('$', _tomato_render_func)
        tomato_col.set_expand(False)
        interrupt_col = util.new_text_col('!', _interrupt_render_func)
        interrupt_col.set_expand(False)

        act_view.append_column(toggle_col)
        act_view.append_column(title_col)
        act_view.append_column(tomato_col)
        act_view.append_column(interrupt_col)

        sel = act_view.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)

        act_model.load_activities()

        return act_view

    def refresh(self):
        self.act_model.load_activities()

    def _on_add(self, widget, *args, **kwargs):
        name = self.act_name.get_text().decode('UTF-8')
        self.act_name.set_text('')
        self.act_model.add_activity(model.Activity(name=name))

    def _on_focus(self, widget, *args, **kwargs):
        name = self.act_name.get_text()
        self.act_name.select_region(0, len(name))

    def _on_toggle_finish(self, renderer, path, user_data=None):
        activity = self.act_model.get_activity_bypath(path)
        if activity.is_finished():
            activity.unfinish()
        else:
            activity.finish()
        self.act_model.update_activity(activity)

    def _on_mark_finish(self, widget):
        (model, it) = self.act_view.get_selection().get_selected()
        activity = model.get_activity_byiter(it)
        if not activity.is_finished():
            activity.finish()
        self.act_model.update_activity(activity)

    def _on_start_timer(self, widget):
        (model, it) = self.act_view.get_selection().get_selected()
        if not it:
            util.show_message_dialog("Please select an activity")
            return
        activity = model.get_activity_byiter(it)
        self.parent_window.hide()
        timer_diag = TimerDialog(activity, finish_callback=self._on_timer_ends)
        timer_diag.show_all()

    def _on_del_activity(self, widget):
        (model, it) = self.act_view.get_selection().get_selected()
        if not it:
            util.show_message_dialog("Please select an activity")
            return
        model.delete_activity_byiter(it)

    def _on_timer_ends(self, tomato, interrupt):
        title = 'Tomato Finished'
        if interrupt:
            title = 'Tomato Interrupted'
        util.show_notification(title, tomato.name)
        self.act_model.finish_tomato(tomato, interrupt)
        self.parent_window.show_all()

    def _on_long_break(self, widget):
        pass



class TimerDialog(gtk.Window):
    """Tomato Timer Dialog"""

    FINISHED = 0
    INTERRUPTED = 1

    TEXT_COLORS = (
            '#1BE01B',
            '#3BE01B',
            '#6BE01B',
            '#9BE01B',
            '#CBE01B',
            '#E0E01B',
            '#E0CB1B',
            '#E09B1B',
            '#E06B1B',
            '#E03B1B',
            '#E01B1B',
            )

    def __init__(self, activity, minutes=25, finish_callback=None):
        super(TimerDialog, self).__init__()
        self.total_minutes = minutes
        self.minutes = minutes
        self.finish_callback = finish_callback
        self.tomato = model.Tomato(activity)
        self.seconds = 0
        self.set_title(activity.name)
        self.set_resizable(False)

        self.time_label = gtk.Label()
        self.time_label.set_tooltip_text(activity.name)
        self.interrupt_button = gtk.Button('Interrupt')
        self.interrupt_button.set_image(gtk.image_new_from_icon_name(
                    'media-playback-stop',
                    gtk.ICON_SIZE_BUTTON))
        self.interrupt_button.set_tooltip_text('Interrupt')
        self.interrupt_button.connect('clicked', self._on_interrupt)
        self.connect('delete-event', self._on_interrupt)
        box = gtk.VBox(False, 2)
        box.pack_start(self.time_label, False, False)
        box.pack_end(self.interrupt_button, False, False)
        self.add(box)
        self._show_time()
        self._timeout_id = gobject.timeout_add(1000, self._update_time)

    def _show_time(self):
        color_idx = (self.total_minutes - self.minutes) * (len(self.TEXT_COLORS) - 1) / self.total_minutes
        color = self.TEXT_COLORS[color_idx]
        self.time_label.set_markup('''<span
                size="50000"
                weight="bold"
                foreground="%s">%02d:%02d</span>'''
                % (color, self.minutes, self.seconds))

    def _update_time(self):
        if self.seconds <= 0:
            self.seconds = 59
            self.minutes = self.minutes - 1
        else:
            self.seconds = self.seconds - 1
        self._show_time()
        if self.minutes < 0:
            self._finish()
            return False
        return True

    def _on_interrupt(self, widget, *args, **kwargs):
        self._finish(interrupt=True)

    def _finish(self, interrupt=False):
        resp_id = self.FINISHED
        if interrupt:
            resp_id = self.INTERRUPTED
        gobject.source_remove(self._timeout_id)
        if self.finish_callback:
            self.finish_callback(self.tomato, interrupt)
        self.destroy()

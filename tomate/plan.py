import pygtk
pygtk.require('2.0')
import gtk

from tomate import model
from tomate import util
from tomate.uimodel import ActivityStore


class PlanView(gtk.VBox):
    """Plan view"""
    def __init__(self, parent_window):
        super(PlanView, self).__init__(False, 3)
        self.parent_window = parent_window
        self.act_name = gtk.Entry()
        self.act_name.set_property('secondary-icon-stock', gtk.STOCK_ADD)
        self.act_name.set_property('secondary-icon-tooltip-text', 'Add new activity')
        self.act_name.set_property('secondary-icon-activatable', True)
        self.act_name.connect('activate', self._on_add)
        self.act_name.connect('icon-press', self._on_add)
        self.act_name.connect('focus-in-event', self._on_focus)

        self.move_button = gtk.Button()
        self.move_button.set_tooltip_text('Move the selected activity to activity view')
        self.move_button.set_image(gtk.image_new_from_icon_name(
                    'media-playback-start', gtk.ICON_SIZE_BUTTON))
        self.move_button.set_relief(gtk.RELIEF_NONE)
        self.move_button.connect('clicked', self._on_move)

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
        new_act_hbox.pack_start(self.move_button, False, False)
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

        act_model = ActivityStore(priority=model.PLANNED)
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

        act_view.append_column(toggle_col)
        act_view.append_column(title_col)

        sel = act_view.get_selection()
        sel.set_mode(gtk.SELECTION_SINGLE)

        act_model.load_activities()

        return act_view

    def _on_add(self, widget, *args, **kwargs):
        name = self.act_name.get_text().decode('UTF-8')
        self.act_name.set_text('')
        self.act_model.add_activity(model.Activity(name=name, priority=model.PLANNED))

    def _on_move(self, widget, *args, **kwargs):
        (_, it) = self.act_view.get_selection().get_selected()
        activity = self.act_model.get_activity_byiter(it)
        activity.priority = model.TODO
        self.act_model.update_activity(activity)

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
        (_, it) = self.act_view.get_selection().get_selected()
        activity = self.act_model.get_activity_byiter(it)
        if not activity.is_finished():
            activity.finish()
        self.act_model.update_activity(activity)

    def _on_del_activity(self, widget):
        (model, it) = self.act_view.get_selection().get_selected()
        if not it:
            util.show_message_dialog("Please select an activity")
            return
        model.delete_activity_byiter(it)


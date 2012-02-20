import pygtk
pygtk.require('2.0')
import gtk
import gobject

from tomate import model

class ActivityStore(gtk.ListStore):

    (TITLE_COL,
     FINISHED_COL,
     TOMATO_COL,
     INTERRUPT_COL,
     ACTIVITY_COL) = range(5)

    def __init__(self, priority=model.TODO):
        super(ActivityStore, self).__init__(str, bool, int, int, gobject.TYPE_PYOBJECT)
        self.priority = priority
        self.store = model.open_store()

    def _append_activity(self, act):
        self.append([act.name,
                     act.finish_time is not None,
                     act.tomatoes,
                     act.interrupts,
                     act])

    def _update_activity(self, act, it):
        self.set_value(it, self.TITLE_COL, act.name)
        self.set_value(it, self.FINISHED_COL, act.finish_time is not None)
        self.set_value(it, self.TOMATO_COL, act.tomatoes)
        self.set_value(it, self.INTERRUPT_COL, act.interrupts)

    def load_activities(self):
        acts = self.store.list_activities(priority=self.priority)
        self.clear()
        for act in acts:
            self._append_activity(act)

    def add_activity(self, act):
        self.store.save_activity(act)
        self._append_activity(act)

    def get_activity_byiter(self, it):
        activity = self.get_value(it, self.ACTIVITY_COL)
        activity._path = self.get_path(it)
        return activity

    def get_activity_bypath(self, path):
        activity = self[path][self.ACTIVITY_COL]
        activity._path = path
        return activity

    def delete_activity_byiter(self, it):
        activity = self.get_value(it, self.ACTIVITY_COL)
        self.store.delete_activity(activity)
        self.remove(it)

    def update_activity(self, act):
        self.store.update_activity(act)
        it = self.get_iter(act._path)
        self._update_activity(act, it)

    def finish_tomato(self, tomato, interrupt):
        if interrupt:
            tomato.interrupt()
        else:
            tomato.finish()
        self.update_activity(tomato.activity)
        self.store.save_tomato(tomato)

    def close(self):
        self.store.archive_activities()
        self.store.close()


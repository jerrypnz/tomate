import pygtk
pygtk.require('2.0')
import gtk
import gobject
from datetime import datetime
from datetime import time
from datetime import timedelta

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


class FinishedTomatoModel(gtk.ListStore):
    (TIME_COL,
     ACTIVITY_COL,
     INTERRUPTED_COL) = range(3)

    def __init__(self):
        super(FinishedTomatoModel, self).__init__(str, str, bool)
        self.store = model.open_store()

    def load_finished_tomatoes(self, date):
        t = time(0, 0, 0)
        start_time = datetime.combine(date, t)
        end_time = start_time + timedelta(days=1)
        tomatoes = self.store.list_tomatoes(start_time, end_time)
        self.clear()
        for tomato in tomatoes:
            start = datetime.fromtimestamp(tomato.start_time).strftime('%H:%M')
            end = datetime.fromtimestamp(tomato.end_time).strftime('%H:%M')
            self.append(('%s - %s' % (start, end), tomato.name, tomato.state == model.INTERRUPTED))



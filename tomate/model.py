from tomate.config import conf

import time
import sqlite3 as sqlite
import os.path

class TomatoError(Exception):
    pass


TODO = 0
PLANNED = 1

class Activity(object):
    """Activity class"""

    def __init__(self, name='Activity', description=None, priority=TODO):
        super(Activity, self).__init__()
        self.id = None # For RDBMS based stores
        self.name = name
        self.description = description
        self.priority = priority
        self.tomatoes = 0
        self.interrupts = 0
        self.finish_time = None

    def add_tomato(self):
        self.tomatoes = self.tomatoes + 1

    def add_interrupt(self):
        self.interrupts = self.interrupts + 1

    def finish(self):
        if self.finish_time:
            raise TomatoError("Activity is already finished")
        self.finish_time = time.time()

    def unfinish(self):
        self.finish_time = None

    def is_finished(self):
        return self.finish_time != None

    def __repr__(self):
        return 'Activity[id=%s, name=%s, priority=%s, tomatoes=%s, interrupts=%s, finish_time=%s]' % (
                self.id, self.name, self.priority, self.tomatoes, self.interrupts, self.finish_time
                )


class Tomato(object):
    """Tomato Class"""
    RUNNING = 0
    FINISHED = 1
    INTERRUPTED = 2

    def __init__(self, activity, duration=25):
        super(Tomato, self).__init__()
        self.id = None # For RDBMS based stores
        self.name = activity.name
        self.activity = activity
        self.duration = duration
        self.state = Tomato.RUNNING
        self.start_time = time.time()
        self.end_time = self.start_time + duration * 60

    def interrupt(self):
        current_time = time.time()
        if current_time >= self.end_time:
            raise TomatoError("The tomato is ended")
        self.state = Tomato.INTERRUPTED
        self.end_time = time.time()
        self.activity.add_interrupt()

    def finish(self):
        current_time = time.time()
        if current_time < self.end_time:
            raise TomatoError("Not finished yet")
        self.state = Tomato.FINISHED
        self.activity.add_tomato()

    def __repr__(self):
        return 'Tomato[id=%s, act=%s, duration=%s, stat=%s, start_time=%s, end_time=%s]' % (
                    self.id, self.name, self.duration, self.state, self.start_time, self.end_time
                )


def open_store():
    filename = conf.get_db_filename()
    return SqliteStore(filename)


class SqliteStore(object):

    TABLES = (
        '''create table activity (
            id integer primary key,
            name text,
            description text,
            priority integer,
            tomatoes integer,
            interrupts integer,
            finish_time integer
        )''',
        '''create table activity_history (
            id integer primary key,
            name text,
            description text,
            tomatoes integer,
            interrupts integer,
            finish_time integer
        )''',
        '''create table tomato (
            id integer primary key,
            name text,
            activity_id integer,
            start_time integer,
            end_time integer,
            state integer
        )''',
        )

    ACT_ROWS = '''id
        ,name
        ,description
        ,priority
        ,tomatoes
        ,interrupts
        ,finish_time'''

    def __init__(self, filename):
        super(SqliteStore, self).__init__()
        db_exists = os.path.exists(filename)
        self.conn = sqlite.connect(filename)
        if not db_exists:
            self._create_tables()

    def _create_tables(self):
        for sql in self.TABLES:
            self.conn.execute(sql)

    @classmethod
    def _map_to_activity(cls, result_tuple):
        act = Activity()
        (act.id,
         act.name,
         act.description,
         act.priority,
         act.tomatoes,
         act.interrupts,
         act.finish_time,
        ) = result_tuple
        return act

    def save_activity(self, activity):
        cur = self.conn.cursor()
        cur.execute('''insert into activity(
                name,
                description,
                priority,
                tomatoes,
                interrupts,
                finish_time) values (
                ?, ?, ?, ?, ?, ?)''', (
                activity.name,
                activity.description,
                activity.priority,
                activity.tomatoes,
                activity.interrupts,
                activity.finish_time,
                )
            )
        self.conn.commit()
        activity.id = cur.lastrowid
        return cur.lastrowid

    def update_activity(self, activity):
        if activity.id is None:
            raise TomatoError('Activity is not saved yet')
        cur = self.conn.cursor()
        cur.execute('''update activity set
                name=?,
                description=?,
                priority=?,
                tomatoes=?,
                interrupts=?,
                finish_time=?
                where id=?''', (
                activity.name,
                activity.description,
                activity.priority,
                activity.tomatoes,
                activity.interrupts,
                activity.finish_time,
                activity.id,
                )
            )
        self.conn.commit()
        return cur.rowcount

    def delete_activity(self, activity):
        if activity.id is None:
            return 0
        cur = self.conn.cursor()
        self._delete_activity(cur, activity.id)
        self.conn.commit()
        return cur.rowcount

    def _delete_activity(self, cur, _id):
        cur.execute('''delete from activity
                where id=?''', (_id,)
            )

    def list_activities(self, priority=TODO):
        cur = self.conn.cursor()
        cur.execute('''select %s from activity
                where priority=?''' % self.ACT_ROWS, (priority,))
        return [ self._map_to_activity(r) for r in cur.fetchall() ]

    def archive_activities(self):
        cur = self.conn.cursor()
        cur.execute('''select %s from activity
                where finish_time is not null''' % self.ACT_ROWS)
        acts = [ self._map_to_activity(r) for r in cur.fetchall() ]
        for act in acts:
            cur.execute('''insert into activity_history(
                    name,
                    description,
                    tomatoes,
                    interrupts,
                    finish_time) values (
                    ?, ?, ?, ?, ?)''', (
                    act.name,
                    act.description,
                    act.tomatoes,
                    act.interrupts,
                    act.finish_time,
                    )
                )
            self._delete_activity(cur, act.id)
        self.conn.commit()

    def get_activity(self, _id):
        cur = self.conn.cursor()
        cur.execute('''select %s from activity
                where id=?''' % self.ACT_ROWS, (_id,))
        r = cur.fetchone()
        if not r:
            return None
        else:
            return self._map_to_activity(r)

    def save_tomato(self, tomato):
        cur = self.conn.cursor()
        act_id = None
        if tomato.activity:
            act_id = tomato.activity.id
        cur.execute('''insert into tomato(
                name,
                activity_id,
                start_time,
                end_time,
                state) values (
                ?, ?, ?, ?, ?)''', (
                tomato.name,
                act_id,
                tomato.start_time,
                tomato.end_time,
                tomato.state,
                )
            )
        self.conn.commit()
        tomato.id = cur.lastrowid
        return cur.lastrowid

    def update_tomato(self, tomato):
        if tomato.id is None:
            raise TomatoError('Tomato is not saved yet')
        cur = self.conn.cursor()
        act_id = None
        if tomato.activity:
            act_id = tomato.activity.id
        cur.execute('''update tomato set
                name=?,
                activity_id=?,
                start_time=?,
                end_time=?,
                state=? where id=?''', (
                tomato.name,
                act_id,
                tomato.start_time,
                tomato.end_time,
                tomato.state,
                tomato.id,
                )
            )
        self.conn.commit()
        return cur.rowcount

    def close(self):
        self.conn.close()


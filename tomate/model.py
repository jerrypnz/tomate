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


from tomate.config import conf

import time
import datetime
import calendar
import sqlite3 as sqlite
import os.path
import itertools

class TomatoError(Exception):
    pass


TODO = 0
PLANNED = 1

RUNNING = 0
FINISHED = 1
INTERRUPTED = 2

def now():
    return round(time.time())

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
        self.finish_time = now()

    def unfinish(self):
        self.finish_time = None

    def is_finished(self):
        return self.finish_time != None

    def __repr__(self):
        return '''Activity[id=%s,
                    name=%s,
                    priority=%s,
                    tomatoes=%s,
                    interrupts=%s,
                    finish_time=%s]''' % (
                self.id,
                self.name,
                self.priority,
                self.tomatoes,
                self.interrupts,
                self.finish_time
                )


class Tomato(object):
    """Tomato Class"""

    def __init__(self, activity=None, duration=25):
        super(Tomato, self).__init__()
        self.id = None # For RDBMS based stores
        name = desc = None
        if activity:
            name = activity.name
            desc = activity.description
        self.activity = activity
        self.name = name
        self.description = desc
        self.duration = duration
        self.state = RUNNING
        self.start_time = now()
        self.end_time = self.start_time + duration * 60

    def interrupt(self):
        current_time = now()
        if current_time >= self.end_time:
            raise TomatoError("The tomato is ended")
        self.state = INTERRUPTED
        self.end_time = now()
        self.activity.add_interrupt()

    def finish(self):
        current_time = now()
        if current_time < self.end_time:
            raise TomatoError("Not finished yet")
        self.state = FINISHED
        self.activity.add_tomato()

    def __repr__(self):
        return '''Tomato[id=%s,
                    act=%s,
                    duration=%s,
                    stat=%s,
                    start_time=%s,
                    end_time=%s]''' % (
                    self.id,
                    self.name,
                    self.duration,
                    self.state,
                    self.start_time,
                    self.end_time
                )


def open_store():
    filename = conf.get_db_filename()
    return SqliteStore(filename)


def datetime2secs(dt):
    '''Convert a datetime object to seconds since epoch in UTC'''
    if isinstance(dt, datetime.datetime):
        return round(time.mktime(dt.utctimetuple()))
    else:
        return dt


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
            priority integer,
            tomatoes integer,
            interrupts integer,
            finish_time integer
        )''',
        '''create table tomato (
            id integer primary key,
            name text,
            description text,
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

    TOMATO_ROWS = '''id
        ,name
        ,description
        ,start_time
        ,end_time
        ,state'''

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

    @classmethod
    def _map_to_tomato(cls, result_tuple):
        t = Tomato(activity=None)
        (t.id,
         t.name,
         t.description,
         t.start_time,
         t.end_time,
         t.state,
        ) = result_tuple
        return t

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
        rowcount = cur.rowcount
        if rowcount > 0:
            cur.execute('''update tomato set
                    name=?,
                    description=?
                    where activity_id=?''', (
                    activity.name,
                    activity.description,
                    activity.id,
                    )
                )
        self.conn.commit()
        return rowcount

    def delete_activity(self, activity):
        if activity.id is None:
            return 0
        cur = self.conn.cursor()
        self._delete_activity(cur, activity.id)
        self.conn.commit()
        return cur.rowcount

    def _delete_activity(self, cur, _id):
        cur.execute('''delete from activity
                where id=?''', (_id,))
        cur.execute('''update tomato set activity_id=null
                where activity_id=?''', (_id,))

    def list_activities(self, priority=TODO):
        cur = self.conn.cursor()
        cur.execute('''select %s from activity
                where priority=?''' % self.ACT_ROWS, (priority,))
        return [ self._map_to_activity(r) for r in cur.fetchall() ]

    def list_finished_activities(self, time1, time2):
        time1 = datetime2secs(time1)
        time2 = datetime2secs(time2)
        cur = self.conn.cursor()
        cur.execute('''select %s from activity
                where finish_time>=? and finish_time<?''' % self.ACT_ROWS, (time1, time2))
        return [ self._map_to_activity(r) for r in cur.fetchall() ]

    def list_activity_histories(self, time1, time2):
        time1 = datetime2secs(time1)
        time2 = datetime2secs(time2)
        cur = self.conn.cursor()
        cur.execute('''select %s from activity_history
                where finish_time>=? and finish_time<?''' % self.ACT_ROWS, (time1, time2))
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
                    priority,
                    tomatoes,
                    interrupts,
                    finish_time) values (
                    ?, ?, ?, ?, ?, ?)''', (
                    act.name,
                    act.description,
                    act.priority,
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
                description,
                activity_id,
                start_time,
                end_time,
                state) values (
                ?, ?, ?, ?, ?, ?)''', (
                tomato.name,
                tomato.description,
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

    def list_tomatoes(self, time1, time2):
        time1 = datetime2secs(time1)
        time2 = datetime2secs(time2)
        cur = self.conn.cursor()
        cur.execute('''select %s from tomato
                where start_time>=? and start_time<?
                and state!=?''' % self.TOMATO_ROWS,
                (time1, time2, RUNNING))
        return [ self._map_to_tomato(r) for r in cur.fetchall() ]

    def statistics_tomato_count(self, time1, time2):
        time1 = datetime2secs(time1)
        time2 = datetime2secs(time2)
        table = self._empty_table(time1, time2)
        data = self._count_tomatoes_by_stat(FINISHED, time1, time2)
        for count, time in data:
            table[time][0] = count
        data = self._count_tomatoes_by_stat(INTERRUPTED, time1, time2)
        for count, time in data:
            table[time][1] = count
        result = list(table.items())
        result.sort()
        return result

    def _count_tomatoes_by_stat(self, stat, time1, time2):
        cur = self.conn.cursor()
        cur.execute('''select count(id),
                round(start_time - start_time % 86400) as day
                from tomato
                where state=?
                and start_time>=? and start_time<?
                group by day
                order by day''', (stat, time1, time2))
        return cur.fetchall()

    def _empty_table(self, time1, time2):
        start = time1 - time1 % 86400
        keys = range(int(start), int(time2), 86400)
        return dict(itertools.izip(keys, ([0,0] for i in range(len(keys)))))

    def close(self):
        self.conn.close()

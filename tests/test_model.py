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


from tomate import model
import time
from datetime import datetime


def test_save_activity(st):
    print "---------------test save activity--------------"
    act = model.Activity('Do this', description='Do this, do that', priority=model.PLANNED)
    act.tomatoes = 2
    act.interrupts = 2
    act_id = st.save_activity(act)
    act.id = act_id
    return act

def test_update_activity(st):
    print "---------------test update activity--------------"
    act = model.Activity('Do that', description='Do this, do that, yes!')
    act_id = st.save_activity(act)
    act.id = act_id
    act.finish_time = time.time()
    act.tomatoes = 8
    act.interrupts = 8
    st.update_activity(act)
    return act

def test_list_activities(st, planned=False):
    txt = planned and 'planned' or 'todo'
    prior = planned and model.PLANNED or model.TODO
    acts = st.list_activities(priority=prior)
    print "----------listing %s activities--------" % (txt)
    for a in acts:
        print a

def test_get_activity(st, _id):
    act = st.get_activity(_id)
    print "----------get activity %s -----------" % _id
    print act

def test_delete_activity(st, act):
    print "activity deleted: ", st.delete_activity(act)
    act.id = None
    return act

def test_save_tomato(st, act):
    print "---------------test save tomato--------------"
    t = model.Tomato(act)
    t_id = st.save_tomato(t)
    t.id = t_id
    return t

def test_update_tomato(st, act):
    print "---------------test update tomato--------------"
    t = model.Tomato(act)
    t_id = st.save_tomato(t)
    t.id = t_id
    t.interrupt()
    st.update_tomato(t)
    return t

def test_archive_activities(st):
    print "--------------test archive history-------------"
    act = model.Activity("Play a game", description="Play Skyrim RPG")
    act.finish()
    st.save_activity(act)
    st.archive_activities()

def test_list_tomatoes(st, time1, time2):
    print "--------------test list tomatoes----------------"
    t_list = st.list_tomatoes(time1, time2)
    for t in t_list:
        print t

def test_list_acthistories(st, time1, time2):
    print "--------------test list activity histories----------------"
    acts = st.list_activity_histories(time1, time2)
    for a in acts:
        print a

def test_statistics_tomato_count(st, time1, time2):
    print "--------------test statistics-----------------------------"
    print st.statistics_tomato_count(time1, time2)

def main():
    st = model.SqliteStore('/tmp/test.db')
    time1 = datetime.now()
    print "Start time: ", model.datetime2secs(time1)
    test_save_activity(st)
    act = test_save_activity(st)
    print act
    print test_update_activity(st)
    test_list_activities(st, planned=True)
    test_list_activities(st, planned=False)
    test_get_activity(st, 1)
    test_get_activity(st, 2)
    test_get_activity(st, 3)
    test_get_activity(st, 4)
    t = test_save_tomato(st, act)
    print t
    print test_update_tomato(st, act)
    test_delete_activity(st, act)
    test_archive_activities(st)
    time.sleep(1)
    time2 = datetime.now()
    print "End time: ", model.datetime2secs(time2)
    test_list_tomatoes(st, time1, time2)
    test_list_acthistories(st, time1, time2)
    test_statistics_tomato_count(st, time1, time2)
    st.close()

if __name__ == '__main__':
    main()

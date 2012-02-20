from tomate import model
import time


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

def main():
    st = model.SqliteStore('/tmp/test.db')
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
    st.close()

if __name__ == '__main__':
    main()

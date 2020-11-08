import os
import json
from random import randrange, randint
from datetime import timedelta, datetime
from wait_time.database import get_db_connection

random_students = """
select * from users where is_professor = 0
order by rand()
limit 30;
"""

get_office_hours = """
select * from office_hours
order by user_id, start
"""

join_meeting = """
insert into attendees (office_hours_id, user_id, lobby_join, current_position, current_estimated_wait_time_seconds)
values (%s, %s, %s, %s, %s)
"""

add_log = """
insert into attendee_log (attendee_id, event_id, event_time)
values
(%s, %s, %s)
"""

add_queue_position = """
insert into attendee_queue_positions (attendee_id, position, estimated_wait_time_seconds, event_time)
values
(%s, %s, %s, %s)
"""

update_attendee = """
update attendees
    set current_position = %s
"""

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def get_next_position(db, office_hour_id):
    position = 1
    sql = """
    select max(current_position) as position from attendees as a
    where office_hours_id = %s
    """
    cur = db.cursor(dictionary=True)
    cur.execute(sql, (office_hour_id, ))
    queue_position = cur.fetchone()
    cur.close()
    if queue_position:
        if queue_position["position"] is not None:
            position = queue_position["position"] + 1
    return position

def get_estimated_wait_time(db, office_hour_id):
    estimated_wait_time = randrange(60, 360, 60)
    sql = """
    select max(current_estimated_wait_time_seconds) as wait_time from attendees as a
    where current_position is not null
    and office_hours_id = %s
    """
    cur = db.cursor(dictionary=True)
    cur.execute(sql, (office_hour_id, ))
    queue = cur.fetchone()
    cur.close()
    if queue:
        if queue["wait_time"] is not None:
            estimated_wait_time = queue["wait_time"] + estimated_wait_time
    return estimated_wait_time

def get_wait_time(db, office_hour_id, position):
    wait_time = int(0)
    sql = """
    select sum(current_estimated_wait_time_seconds) as wait_time
    from attendees
    where office_hours_id = %s
    and current_position < %s
    """
    cur = db.cursor(dictionary=True)
    cur.execute(sql, (office_hour_id, position))
    queue = cur.fetchone()
    if queue:
        if queue["wait_time"] is not None:
            wait_time = int(queue["wait_time"])
    cur.close()
    return wait_time

db = get_db_connection(read_only=False)

cur = db.cursor(dictionary=True)


"""
cur.execute(get_office_hours)
office_hours = cur.fetchall()
cur.execute(random_students)
students = cur.fetchall()

for student in students:
    for office_hour in office_hours:
        # add the attendee record
        random_join = random_date(office_hour["start_time"], office_hour["end_time"])
        
        position = get_next_position(db, office_hour["id"])
        estimated_wait_time = get_estimated_wait_time(db, office_hour["id"])

        cur.execute(join_meeting, (office_hour["id"], student["id"], random_join, position, estimated_wait_time))
        attendee_id = cur.lastrowid
        print(f"attendee id: {attendee_id}")
        # add join event to log
        cur.execute(add_log, (attendee_id, 1, random_join))
        # setup the users position
        cur.execute(add_queue_position, (attendee_id, position, estimated_wait_time, random_join))
"""


cur.execute("select * from attendees")
attendees = cur.fetchall()
for attendee in attendees:
    print(attendee)
    for i in range(attendee["current_position"], 0, -1):
        wait_time = get_wait_time(db, attendee["office_hours_id"], i)
        event_time = attendee["lobby_join"] - timedelta(seconds=wait_time)
        cur.execute(add_queue_position, (attendee["id"], i - 1, wait_time, event_time))
        print(i)
    cur.execute(add_log, (attendee["id"], 2, event_time))
    estimated_wait_time = randrange(60, 360, 60)
    event_time = event_time - timedelta(seconds=estimated_wait_time)
    cur.execute(add_log, (attendee["id"], 3, event_time))
    cur.execute(add_log, (attendee["id"], 4, event_time))




db.commit()
cur.close()
db.close()
print("we are complete")
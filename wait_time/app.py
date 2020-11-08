import os
import json
from database import get_db_connection

def get_avg_session_time(student_id, professor_id):
    SQL = """
    """
def get_attendee_info(db, attendee_id):
    SQL = """
    select
        p.id as professor_id, 
        concat(p.first_name, ' ', p.last_name) as professor_name, 
        s.id as student_id, 
        concat(s.first_name, ' ', s.last_name) as student_name
    from attendees as a
    inner join users as s on a.user_id = s.id
    inner join office_hours as oh on a.office_hours_id = oh.id
    inner join users as p on oh.user_id = p.id
    where a.id = %s
    """
    cur = db.cursor()
    cur.execute(SQL, (attendee_id, ))
    attendee = cur.fetchone()
    cur.close()
    return attendee

def lambda_handler(event, context):
    body = event
    attendee_id = body["attendee_id"]
    db = get_db_connection(read_only=False)
    info = get_attendee_info(db, attendee_id)
    db.close()
    print(info)
    print(attendee_id)
    return {"wait_time": 200}
    

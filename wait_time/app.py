import json
# import requests

def lambda_handler(event, context):
    body = event
    attendee_id = body["attendee_id"]
    print(attendee_id)
    return {"wait_time": 200}
    

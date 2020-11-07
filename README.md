# StudyEdgeOfficeHours

## Installation
Make sure you have python3 and sam installed


To ensure everything is setup correctly:
```
sam validate
```

Run it like this:
```
echo '{"attendee_id": 22}' |  sam local invoke "WaitTimeFunction" -e -
```
where 22 above represents an attendee_id

Each time you make a code change you need to run:
```
sam build
```

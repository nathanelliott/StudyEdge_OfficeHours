# StudyEdgeOfficeHours

## Installation
Make sure you have python3 and sam installed


Set your local environment varibles in your terminal session:
```
export MYSQL_USER=<dbusername>
export MYSQL_PASSWD=<dbpassword>
export MYSQL_HOST=<dbhostname>
```

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

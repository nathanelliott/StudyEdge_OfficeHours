import os
import logging
from mysql.connector import connection

# LOGGER = logging.getLogger()

def get_db_connection(read_only=True):
    # LOGGER.info("Opening DB connection host=%s", MYSQL_HOST)
    return connection.MySQLConnection(host=os.getenv('MYSQL_HOST'),
                                      user=os.getenv('MYSQL_USER'),
                                      password=os.getenv('MYSQL_PASSWD'),
                                      database="office_hours",
                                      buffered=True,
                                      connection_timeout=10)


from datetime import datetime
import sys
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
import uuid

user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# RDS Data connection
try:
    conn = psycopg2.connect(host=rds_proxy_host, user=user_name,
                            password=password, database=db_name, connect_timeout=5)
    conn.autocommit = True

except Exception as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to Postgres instance.")
    print(e)
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS for Postgres instance succeeded")


def lambda_handler(event, context):

    try:
        records = event['Records']

        for record in records:
            email = record['messageAttributes']['Email']['stringValue']
            username = record['messageAttributes']['Username']['stringValue']
            password = record['messageAttributes']['Password']['stringValue']

        salt = str(uuid.uuid4().hex)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            'SELECT id FROM public.user WHERE username = %s OR email = %s', (username, email))
        result = cur.fetchall()
        json_data = json.dumps(result)

        if json_data == '[]':
            logger.info(
                'User {0} does not exist in the database'.format(username))
            cur.execute('INSERT INTO public.user (username, email, password, salt) VALUES (%s, %s, %s, %s)',
                        (username, email, password, salt))
            conn.commit()
            return 'User {0} created successfully'.format(username)
        else:
            logger.info(
                'User {0} already exists in the database'.format(username))
            return 'User {0} already exists in the database'.format(username)

    except Exception as e:
        logger.error("ERROR: Unexpected error")
        logger.error(e)
        sys.exit()

import psycopg2
import os
from dotenv import load_dotenv

from models import CourtCase

load_dotenv(dotenv_path="../../.env.dev")

def get_connection():
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        host = os.getenv("DB_HOST"),
        port = os.getent("DB_HOST)")
    )

def get_court_id_by_city(city):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM court WHERE name = %s
                """,
                 (city))
            row = cur.fetchone()
            return row[0] if row else None
        
def insert_court_case(court_case:CourtCase, court_id):
    conn = get_connection()
    with conn:
        with conn.cursor_factory as cur:
            cur.execute(
                '''
                    INSERT INTO court_case(
                    start_time_epoch,
                    duration,
                    case_id,
                    claimant,
                    defendant,
                    hearing_type,
                    hearing_channel,
                    court_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''',
                (
                    court_case.start_time_epoch,
                    court_case.duration,
                    court_case.case_id,
                    court_case.claimant,
                    court_case.defendant,
                    court_case.hearing_type,
                    court_case.hearing_channel,
                    court_id
                )
            )
    return cur.fetchone()[0] # is it useful to return the case id? maybe for testing? leave in for now.
import psycopg2
import os
from dotenv import load_dotenv

from db.models import CourtCase

load_dotenv(dotenv_path="../.env.dev", override=True) # override means that it removes any lingering .env vars

def get_connection():
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )

    

def get_court_id_by_city(city):
    conn = get_connection()  
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id FROM court WHERE city = %s
                    """,
                    (city,)) #trailing comma is important as execute needs a tuple as arg, and that is how to designate
                row = (cur.fetchone())
                return row[0] if row else None
                

    finally:
       conn.close()
        
def insert_court_case(court_case:CourtCase, court_id):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
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
        
    except psycopg2.IntegrityError as e:
        # print(f"case already exists?: {court_case}\n {e.with_traceback}")
        pass

    finally:
        conn.close()

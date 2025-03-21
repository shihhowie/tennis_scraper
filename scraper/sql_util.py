import psycopg2

DB_NAME="testdb"
DB_USER="howardshih"
DB_PASSWORD="howardshih"

DB_HOST="database-1.c12cmowoyxgf.eu-north-1.rds.amazonaws.com"
DB_PORT="5432"

def write_to_db(sql):
    try:
        # SQL = """
        #    INSERT INTO tennis_court_schedule (name, req_time, req_date, start_time, end_time, num_slots) 
        #    VALUES ('test_court', 0000, '20250316', '20250316', '20250316', 3);
        # """
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        # print("commited SQL: ", sql)
        cur.close()
        conn.close()
    except Exception as e:
        print("ERROR:", e)


if __name__ == '__main__':
    connect_to_db()
    write_to_db()

import psycopg2

DB_NAME="testdb"
DB_USER="howardshih"
DB_PASSWORD="howardshih"

DB_HOST="database-1.c12cmowoyxgf.eu-north-1.rds.amazonaws.com"
DB_PORT="5432"

def connect_to_db():
    try:
    # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to the database successfully!")

        # Create a cursor object
        cur = conn.cursor()

        # Execute a SQL query to fetch table data
        cur.execute("SELECT * FROM tennis_court_schedule LIMIT 5;")
        rows = cur.fetchall()

        # Print the results
        for row in rows:
            print(row)

        # Close connection
        cur.close()
        conn.close()
        print("Connection closed.")

    except Exception as e:
        print("Error:", e)


def write_to_db(sql):
    try:
        # SQL = """
        #    INSERT INTO tennis_court_schedule (name, req_time, req_date, start_time, end_time, num_slots) 
        #    VALUES ('test_court', 0000, '20250316', '20250316', '20250316', 3);
        # """
        conn = psycopg2.connect(
            dbname=DB_NAME,
                                                                                                                                               25,10         50%
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_NAME="testdb"
DB_USER="howardshih"
DB_PASSWORD="howardshih"

DB_HOST="database-1.c12cmowoyxgf.eu-north-1.rds.amazonaws.com"
DB_PORT="5432"

url_lookup = {
    "rosemary_garden_tennis": "https://bookings.better.org.uk/location/islington-tennis-centre/rosemary-gardens-tennis/",
    "islington_tennis_centre": "https://bookings.better.org.uk/location/islington-tennis-centre/tennis-court-indoor/"
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Tennis Court API is running"}), 200

@app.route('/api/availability', methods=['GET'])
def get_availability():
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
        
        sql = """
            select * from (select *, RANK() over (partition by name order by req_time desc) 
            from tennis_court_schedule) 
            where rank=1;
        """
        # Execute a SQL query to fetch table data
        cur.execute(sql)
        rows = cur.fetchall()

        # Print the results
        results = []
        for row in rows:
            date_str = row[2].strftime("%Y-%m-%d")
            url = f"{url_lookup.get(row[0])}/{date_str}"
            pack_line = {"court": row[0], "date": row[2], "start": row[3], "end": row[4], "slots": row[5], "url": url}
            results.append(pack_line)
            # print(pack_line)
        # Close connection
        cur.close()
        conn.close()
        print("Connection closed.")
        # print(results)
        print("jsonify res", jsonify(results))
        return jsonify(results)

    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    # get_availability()
    app.run(host='0.0.0.0', port=5000)
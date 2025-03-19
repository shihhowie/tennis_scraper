import psycopg2
from flask import Flask, jsonify
from datetime import datetime
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver

# app = Flask(__name__)
app = ApiGatewayResolver()

DB_NAME="testdb"
DB_USER="howardshih"
DB_PASSWORD="howardshih"

# DB_HOST="database-1.c12cmowoyxgf.eu-north-1.rds.amazonaws.com"
DB_HOST="hshih-db-eu1.proxy-c12cmowoyxgf.eu-north-1.rds.amazonaws.com"
DB_PORT="5432"

url_lookup = {
    "rosemary_garden_tennis": "https://bookings.better.org.uk/location/islington-tennis-centre/rosemary-gardens-tennis",
    "islington_tennis_centre": "https://bookings.better.org.uk/location/islington-tennis-centre/tennis-court-indoor"
}

@app.get("/")
def home():
    return {"message": "Tennis Court API is running"}

@app.get('/api/availability')
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
            date_str = datetime.strptime(str(row[2]), "%Y%m%d").strftime("%Y-%m-%d")
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
        return results

    except Exception as e:
        print("Error:", e)

# Lambda handler
def lambda_handler(event, context):
    print("Received event:", event)

    # Extract the HTTP method and path for HTTP API (Version 2)
    if "httpMethod" not in event and "requestContext" in event:
        event["httpMethod"] = event["requestContext"]["http"]["method"]
        event["path"] = event["rawPath"]
        
    return app.resolve(event, context)

# if __name__ == '__main__':
#     # get_availability()
#     # app.run(host='0.0.0.0', port=5000)
#     app.resolve(event, context)
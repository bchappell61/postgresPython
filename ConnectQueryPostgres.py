# Bill Chappell 2020
# This was a simple script to export some fields out of a Postgres/PostGIS 
# Database for a selected record based on an address.

#pip install psycopg2
import psycopg2

conn = None

print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(
    host="localhost",
    database="<databaseName>",
    user="postgres",
    password="<thePassword>",
    port="5432"
    )

# Query for:
address = "1863 Mill Rd"

# Query table for attributes The ? is a placeholder for a variable
sql = """SELECT address, fixture_ty, pole_id
         FROM lights
         WHERE lights.address = (%s); """

print('Connecting to the PostgreSQL database...')

# create a cursor
cur = conn.cursor()

# address is the variable for the placeholder in sql query
cur.execute(sql,(address,)) # Note comma after address needed Tuple

# Fetchone brings back the matching record for that ID number
result = cur.fetchone()

print(result)
#('1863 Mill Rd', 'Cobra', 21.0)

# close the communication with the PostgreSQL
cur.close()
conn.close()
print('Database connection closed.')


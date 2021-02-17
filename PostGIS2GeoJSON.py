
# Bill Chappell 2020
# This was a simple script to export some fields out of a Postgres/PostGIS 
# Database. My X,Y coordinates were in a geog field and I used the ST_X & ST_Y functions.
# This creates a simple Point eoJSON file. Some of the code was found at
# https://geoffboeing.com/2015/10/exporting-python-data-geojson

import psycopg2
import json
import pandas as pd

def df_to_geojson(df, properties):

    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():

        lat = col.index('latitude')
        lon = col.index('longitude')
        
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
                              
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for i in properties:
            x = col.index(i)
            feature['properties'][i] = row[x]
        geojson['features'].append(feature)
    return geojson


conn = None

print('Connecting to the PostgreSQL database...')

# Connect to the database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="<databaseName>",
        user="postgres",
        password="<thePassword>",
        port="5432"
        )

except:
    print( "Unable to connect to the database. Please check your options and try again.")
          

# SQL query, Lat, Long, are stored in a Geography type field called geog
sql = """SELECT address, fixture_ty, pole_id, ST_X(geog::geometry) As longitude, ST_Y(geog::geometry) As latitude
         FROM lights; """

# create a cursor
cur = conn.cursor()

# Connect to database
cur.execute(sql) 

# Get the response
res = cur.fetchall()

# Get the column names returned
col = [name[0] for name in cur.description]

# Create a DataFrame
df = pd.DataFrame(res)

# Pass the Dataframe and columns list to function, data returned is places in geojson var
geojson = df_to_geojson(df, col)

# Create GeoJSON formatted file
output_filename = 'GeoJSON_Pts.geojson'
with open(output_filename, 'w') as output_file:
    json.dump(geojson, output_file, indent=2)

# close the communication with the PostgreSQL
cur.close()
conn.close()
print('Database connection closed. Finished.')

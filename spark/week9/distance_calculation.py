import json
import pyspark
import pprint
from operator import add
from math import cos, sin, asin, sqrt, radians

sc = pyspark.SparkContext()
 
bucket = sc._jsc.hadoopConfiguration().get('fs.gs.system.bucket')
project = sc._jsc.hadoopConfiguration().get('fs.gs.project.id')

input_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_input'.format(bucket)
output_directory = 'gs://{}/pyspark_demo_output'.format(bucket)

conf = {
    'mapred.bq.project.id': project,
    'mapred.bq.gcs.bucket': bucket,
    'mapred.bq.temp.gcs.path': input_directory,
    'mapred.bq.input.project.id': 'cs512-week7',
    'mapred.bq.input.dataset.id': 'pings',
    'mapred.bq.input.table.id': 'pings'
}

table_data = sc.newAPIHadoopRDD(
    'com.google.cloud.hadoop.io.bigquery.JsonTextBigQueryInputFormat',
    'org.apache.hadoop.io.LongWritable',
    'com.google.gson.JsonObject',
    conf=conf
)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def getHaversineDistance(pings):
    distance = 0
    # The zip() in python returns an iterable of tuples... very handy!
    for start, end in zip(pings, pings[1:]):
        distance += haversine(
            float(start[1]['Long']), float(start[1]['Lat']),
            float(end[1]['Long']), float(end[1]['Lat'])
        )
    return distance

# Get values from Big Query Table
vals = table_data.values().map(lambda line: json.loads(line))
# vals = vals.map(lambda line: json.loads(line))
key_pings = vals.map(lambda x: (x['Icao'], x))
sorted_key_pings = key_pings.sortBy(lambda x: x[1]['PosTime'])

grouped_key_pings = sorted_key_pings.groupBy(lambda x: x[0])

grouped_key_pings_lst = grouped_key_pings.map(lambda (x, y): (x, list(y)))
distances = grouped_key_pings_lst.map(lambda (x,y): (x, getHaversineDistance(y)))

totalDistance = distances.map(lambda (x,y): y).reduce(add)
pprint.pprint("The total distance flown is: " + str(totalDistance) +" km.")
sc.parallelize([totalDistance]).saveAsTextFile(output_directory)

sortedDistance = distances.sortBy(lambda x: x[1], ascending = False)

print("The flights that had the longest distance were:")
pprint.pprint(sortedDistance.take(10))


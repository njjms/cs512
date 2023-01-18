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
    'mapred.bq.input.project.id': 'final-reddit-analysis',
    'mapred.bq.input.dataset.id': 'reddit-comments',
    'mapred.bq.input.table.id': 'reddit-comments'
}

table_data = sc.newAPIHadoopRDD(
    'com.google.cloud.hadoop.io.bigquery.JsonTextBigQueryInputFormat',
    'org.apache.hadoop.io.LongWritable',
    'com.google.gson.JsonObject',
    conf=conf
)

vals = table_data.values().map(lambda line: json.loads(line))



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


#!/usr/bin/python
from pyspark.sql import SparkSession

spark = SparkSession \
            .builder \
            .master('yarn') \
            .appName('final-reddit-analysis') \
            .getOrCreate()

# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the connector.
bucket = "reddit-temp"
spark.conf.set('temporaryGcsBucket', bucket)

# Load data from BigQuery.
comments = spark.read.format('bigquery') \
        .option('table', 'final-reddit-analysis:reddit_comments.reddit_comments') \
        .load()
comments.createOrReplaceTempView('comments')

# Perform word count.
comment_query = spark.sql(
    'SELECT string_field_5 as sub, COUNT(string_field_1) as n_users FROM comments GROUP BY sub ORDER BY n_users DESC LIMIT 20'
)
comment_query.show()
comment_query.printSchema()

# Saving the data to BigQuery
comment_query.write.format('bigquery') \
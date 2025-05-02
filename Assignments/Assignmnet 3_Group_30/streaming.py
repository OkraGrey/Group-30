from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# session initialization
spark = SparkSession.builder \
    .appName("TrafficMonitoring") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5") \
    .getOrCreate()

# Reading data from Kapfa that is written in our producer
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic_data") \
    .load()

# Define schema for JSON parsing
schema = StructType([ # Format of data (same as in our prod)
    StructField("sensor_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("vehicle_count", IntegerType()),
    StructField("average_speed", FloatType()),
    StructField("congestion_level", StringType())
])
parsed_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# DATA QUALITY CHECKS GIVEN IN THE PART 3
cleaned_df = parsed_df.filter(
    (col("sensor_id").isNotNull()) &
    (col("timestamp").isNotNull()) &
    (col("vehicle_count") >= 0) &
    (col("average_speed") > 0)
).dropDuplicates(["sensor_id", "timestamp"])

# Traffic Volume per Sensor (5-minute window)
traffic_volume = cleaned_df \
    .withWatermark("timestamp", "5 minutes") \
    .groupBy(
        window("timestamp", "5 minutes"),
        "sensor_id"
    ).agg(sum("vehicle_count").alias("total_vehicles"))

# Part 4 of assignment -> Writing back to kakfa
query = traffic_volume \
    .selectExpr("CAST(sensor_id AS STRING) AS key", "to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "traffic_analysis") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start()

query.awaitTermination()
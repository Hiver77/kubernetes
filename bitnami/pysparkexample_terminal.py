from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, sum, max, min

spark = SparkSession.builder \
    .appName("RandomDataAggregation") \
    .master("spark://spark-release-master-svc:7077") \
    .config("spark.submit.deployMode","cluster") \
    .getOrCreate()
for i in range(0,10):
    data = [
        (i, f"name_{i}", i % 3)  # Simple schema: id, name, category
        for i in range(100000)
    ]
    df = spark.createDataFrame(data, ["id", "name", "category"])
    count_result = df.count()
    avg_id = df.select(avg("id")).collect()[0][0]
    sum_id = df.select(sum("id")).collect()[0][0]
    max_id = df.select(max("id")).collect()[0][0]
    min_id = df.select(min("id")).collect()[0][0]
    print("Count:", count_result)
    print("Average ID:", avg_id)
    print("Sum of IDs:", sum_id)
    print("Maximum ID:", max_id)
    print("Minimum ID:", min_id)
    grouped_df = df.groupBy("category").agg(
        count("id").alias("count"),
        avg("id").alias("avg_id"),
        sum("id").alias("sum_id")
    )
    grouped_df.show()


from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, sum, max, min

# Create a SparkSession
spark = SparkSession.builder.appName("RandomDataAggregation").getOrCreate()

for i in range(0,10):
# Generate 1 million rows of random data
    data = [
        (i, f"name_{i}", i % 3)  # Simple schema: id, name, category
        for i in range(100000)
    ]

    # Create a PySpark DataFrame
    df = spark.createDataFrame(data, ["id", "name", "category"])

    # Basic aggregations
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

    # Group by and aggregate
    grouped_df = df.groupBy("category").agg(
        count("id").alias("count"),
        avg("id").alias("avg_id"),
        sum("id").alias("sum_id")
    )

    grouped_df.show()


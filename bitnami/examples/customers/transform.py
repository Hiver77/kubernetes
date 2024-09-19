import re
from pyspark.sql.functions import col, count, lower, md5, date_format
from pyspark.sql import DataFrame as SparkDF


def read_file(spark, file_path):
    return spark.read.csv(file_path, header=True)

def lowercase(df: SparkDF) -> SparkDF:
    """
    Define la función para validar el correo electrónico
    :param: valor del correo electrónico
    """
    return df.withColumn("First Name", lower(col("First Name"))) \
             .withColumn("Last Name", lower(col("Last Name"))) 

def hash_values(df: SparkDF) -> SparkDF:
    return df.withColumn("Phone 1", md5(col("Phone 1"))) \
             .withColumn("Phone 2", md5(col("Phone 2")))

def email_validation(email: str) -> bool:
    """
    Define la función para validar el correo electrónico
    :param: valor del correo electrónico
    """
    if email is None:
        return False
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def url_validation(url: str) -> bool:
    """
    Define la función para validar la URL
    :param: valor de la url
    """
    if url is None:
        return False
    pattern = r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def customers_per_website_and_country(df: SparkDF) -> SparkDF:
    return df.groupBy('Website', 'Country') \
            .agg(count(col('Customer Id')) \
            .alias('total_customers_website_per_country')) \
            .orderBy('Country')

def customers_per_website_and_date(df: SparkDF) -> SparkDF:
    return df.groupBy('Website', 'Subscription Date') \
            .agg(count(col('Customer Id')) \
            .alias('total_customers_website_per_date')) \
            .orderBy('Website')

def create_partition(df: SparkDF) -> SparkDF:
    return df.withColumn("year", date_format(col("Subscription Date"), "yyyy")) \
             .withColumn("month", date_format(col("Subscription Date"), "MM"))
     

def write_file(df: SparkDF):
    partition_cols = ['year', 'month']
    df.write.partitionBy(*partition_cols) \
        .mode("overwrite") \
        .parquet("/opt/bitnami/spark/tmp/customers")

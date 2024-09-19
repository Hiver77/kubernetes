import sys
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BooleanType
from config import *
from transform import *


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(APP_NAME)

# Create a SparkSession
spark = SparkSession.builder.appName(APP_NAME).getOrCreate()

logger.info("Reading File")
df_customer = read_file(spark, FILE_PATH)

logger.info("Show explain Plan")
df_customer.explain()

logger.info("count Email")
df_customer.select('email').count()

logger.info("count Email")
df_customer.select('Website').count()

logger.info("Show explain Plan")
df_customer.explain()

# Crea la UDF
validar_email_udf = udf(email_validation, BooleanType())
validar_url_udf = udf(url_validation, BooleanType())

df_customer = df_customer.withColumn("email_validated", validar_email_udf(df_customer["email"])) \
                         .filter(col('email_validated') == True).drop(col('email_validated'))
df_customer = df_customer.withColumn("url_validated", validar_url_udf(df_customer["Website"])) \
                         .filter(col('email_validated') == True).drop(col('email_validated'))

logger.info("Show explain Plan")
df_customer.explain()

df_customer.select('email').count()
df_customer.select('Website').count()

logger.info("Show explain Plan")
df_customer.explain()

df_customer = lowercase(df_customer)
df_customer = hash_values(df_customer)

logger.info("Show explain Plan")
df_customer.explain()

logger.info("Group by website and subscription date")
df_customer_website = customers_per_website_and_date(df_customer)
df_customer_website.show(20, truncate=False)

logger.info("Group by total customers website per date")
df_customer_website.groupBy('total_customers_website_per_date') \
                   .count().orderBy('total_customers_website_per_date') \
                   .show()

logger.info("Show explain Plan")
df_customer_website.explain()


df_customer_website.filter(col('total_customers_website_per_date') >= 5) \
                   .show()

logger.info("Show explain Plan")
df_customer_website.explain()

logger.info("Group by website and country")
df_customer_country = customers_per_website_and_country(df_customer)
df_customer_country.show(20, truncate=False)

logger.info("Group by country")
df_customer_country.groupBy('Country') \
                   .count().orderBy('Country') \
                   .show()

logger.info("Show explain Plan")
df_customer_country.explain()

logger.info("Writing Dataframe")
write_file(create_partition(df_customer))
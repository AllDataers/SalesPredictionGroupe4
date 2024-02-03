from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import col,sum
import matplotlib.pyplot as plt

# Create a SparkSession
spark = SparkSession.builder \
    .appName("CSV-Load") \
    .config("spark.sql.warehouse.dir", "file:///C:/temp") \
    .config("spark.hadoop.validateOutputSpecs", "false") \
    .getOrCreate()


# Read CSV file into a Spark DataFrame
# You can specify various options like header, delimiter, etc., using options()
df = spark.read.options(header=True, inferSchema=True).csv("")

# Show the DataFrame schema and a few rows
# df.printSchema()
df.show()
df.where(col("Order ID").isNull()).show()
df2 = df.withColumnRenamed("Order ID","OrderID")\
    .withColumnRenamed("Quantity Ordered","QuantityOrdered")\
    .withColumnRenamed("Price Each","PriceEach")\
    .withColumnRenamed("Order Date","OrderDate")\
    .withColumnRenamed("Purchase Address","PurchaseAddress")\
    .na.drop(subset=["OrderID"])

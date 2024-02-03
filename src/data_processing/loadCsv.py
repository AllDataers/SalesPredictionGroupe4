from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import col,sum
import matplotlib.pyplot as plt

jdbc_url = "jdbc:mysql://your_database_host:port/database_name"
table_name = "your_table_name"
properties = {
    "user": "your_username",
    "password": "your_password",
    "driver": "com.mysql.jdbc.Driver"  # Adjust based on your database
}

# Create a SparkSession
spark = SparkSession.builder \
    .appName("CSV-Load") \
    .config("spark.sql.warehouse.dir", "file:///C:/temp") \
    .config("spark.hadoop.validateOutputSpecs", "false") \
    .getOrCreate()
# %%
# Define the path to your CSV file
csv_file_path = "C:/Users/pc/Desktop/alldataers/SalesPredictionGroupe4/data/raw/Sales_April_2019.csv"

print(csv_file_path)

# %%
# Read CSV file into a Spark DataFrame
# You can specify various options like header, delimiter, etc., using options()
df = spark.read.options(header=True, inferSchema=True).csv(csv_file_path)

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

df2.write \
    .jdbc(url=jdbc_url, table=table_name, mode="overwrite", properties=properties) 

pandasDataframe = df2.groupBy("OrderID")\
.agg(sum("QuantityOrdered")\
     .alias('TotalQuantity'))\
.where(col("TotalQuantity")>=3)\
.sort(col("TotalQuantity").desc())\
.limit(5)\
.toPandas()

print(pandasDataframe)

pandasDataframe.plot(kind='bar',x='OrderID', y='TotalQuantity')
plt.show()

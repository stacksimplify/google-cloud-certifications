#! /usr/bin/python
import pyspark

# Create Number List
numbers = [1,2,3,1,2,3,4,4,2,3,6,6,7,2,2,1,3,4,5,8,1,2]

# Python SparkContext
sc = pyspark.SparkContext()

# Create RDD with parallelize method of SparkContext
rdd = sc.parallelize(numbers)

# Return distinct elements from RDD
distinct_numbers = rdd.distinct().collect()

# Print distinct numbers which we can verify in Cloud Dataproc Logs
print('Distinct Numbers:', distinct_numbers)
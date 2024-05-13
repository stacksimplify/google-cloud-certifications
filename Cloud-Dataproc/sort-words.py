import pyspark

sc = pyspark.SparkContext()
rdd = sc.parallelize(["orange", "pear", "date", "grape", "banana", "kiwi", "cherry", "fig", "lemon", "mango", "apple"])
words = sorted(rdd.collect())
print(words)



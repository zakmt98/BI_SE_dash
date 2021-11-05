from pyspark import SparkConf,SparkContext
import findspark
findspark.init() 
conf = SparkConf().setAppName("read file")
sc = SparkContext.getOrCreate(conf=conf)
sc.setLogLevel("INFO")
print('spark worked')

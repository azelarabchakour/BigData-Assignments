from pyspark import SparkContext, SparkConf
import random

#------------------ Intialize Spark Context ----------------------
conf = SparkConf().setAppName("Task1").setMaster("local[*]")
sc = SparkContext(conf=conf)
#----------------------------------------------------------------

#--------------------- Task 1(a)---------------------------------
list = list(range(0, 80001)) 
rdd = sc.parallelize(list, 8)
even_rdd = rdd.filter(lambda x: x % 2 == 0) 
result = even_rdd.take(7) 
print(result)
#----------------------------------------------------------------

#--------------------- Task 1(b)---------------------------------
random_list = []
for _ in range(40000):
    random_list.append(random.randint(1, 100))

random_rdd = sc.parallelize(random_list, 10)

def get_bucket(number):
    lower_bound = ((number - 1) // 10) * 10 + 1
    upper_bound = lower_bound + 9
    return f"{lower_bound}-{upper_bound}"

bucket_counts_rdd = random_rdd.map(lambda x: (get_bucket(x), 1)).reduceByKey(lambda a, b: a + b)

final_buckets = bucket_counts_rdd.collect()
final_buckets.sort(key=lambda x: int(x[0].split('-')[0]))

for result in final_buckets:
    print(result)
#----------------------------------------------------------------

#--------------------- Task 1(c)---------------------------------

#----------------------------------------------------------------

#--------------------- Task 1(d)---------------------------------

#----------------------------------------------------------------

#--------------------- Task 1(e)---------------------------------

#----------------------------------------------------------------

#------------------ Stop Spark Context --------------------------
sc.stop()
#----------------------------------------------------------------
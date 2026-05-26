from pyspark import SparkContext, SparkConf
import random
from pyspark.ml.feature import StopWordsRemover

#------------------ Intialize Spark Context ----------------------
conf = SparkConf().setAppName("Task1").setMaster("local[*]")
sc = SparkContext(conf=conf)
#----------------------------------------------------------------

#--------------------- Task 1(a)---------------------------------
def task1a():
    numbers_list = list(range(0, 80001)) 
    rdd = sc.parallelize(numbers_list, 8)
    even_rdd = rdd.filter(lambda x: x % 2 == 0) 
    result = even_rdd.take(7) 
    print(result)
#----------------------------------------------------------------


#--------------------- Task 1(b)---------------------------------
def task1b():
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
"""
- The parallelize() function is a PySpark function that takes a 
local Python collection to create an RDD.
- Resilient Distributed Dataset (RDD) is collection of data objects that can be manipulated in parallel, 
Resilient(can recover from node failures automatically), Distributed(data is spread across multiple workers), 
Dataset(it's a read-only collection of records).
- In Task1(a) we create a list with numbers ranging from 0 to 80000, then we split that list across 
8 different partitions of an RDD using parallelize() function, then we register the lambda function to filter for just the 
even numbers but it won't compute anything until we use .take(7) to get the first 7 results.
- The difference between Python filter() and RDD's filter() is that the Python function executes in linear and 
directly. In contrast, RDD's function executes in parallel and lazy. Thus, the RDD's filter() can scale horizantally
unlike the Python's filter() that is limited by vertical scalling.
"""
#----------------------------------------------------------------


#--------------------- Task 1(d)---------------------------------
def task1d():
    rdd = sc.textFile("Text-data.txt")

    def clean_word(word):
        cleaned = ''.join(char for char in word if char.isprintable() and char.isalpha())
        return cleaned.lower().strip()

    words_list = rdd.flatMap(lambda line: line.split()).map(clean_word).filter(lambda word: len(word) > 0)
    word_counts = words_list.map(lambda word : (word,1)).reduceByKey(lambda a, b: a + b)
    top_25_words = word_counts.takeOrdered(25, key=lambda x: -x[1])
    for result in top_25_words:
        print(result)
    return word_counts
#----------------------------------------------------------------


#--------------------- Task 1(e)---------------------------------
def task1e(word_counts):
    # stop_words = {
    #     "the", "and", "of", "to", "a", "in", "that", "is", "was", "for", 
    #     "it", "with", "as", "by", "on", "be", "this", "are", "from", "or",
    #     "not", "at", "but", "an", "had", "which", "he", "his", "they", "we",
    #     "you", "their", "were", "all", "one", "can", "would", "could", "may"
    # }     
    stop_words = set(StopWordsRemover.loadDefaultStopWords("english"))  
    meaningful_words = word_counts.filter(lambda x: x[0] not in stop_words)
    ordered_meaningful_words = meaningful_words.sortBy(lambda x: x[1], ascending=False)
    final_meaningful_words = ordered_meaningful_words.take(30)
    for result in final_meaningful_words:
        print(result)
#----------------------------------------------------------------


#------------------ Execution -----------------------------------
print("----------------------------- TASK a ----------------------\n")
task1a()
print("----------------------------- TASK b ----------------------\n")
task1b()
print("----------------------------- TASK d ----------------------\n")
word_list = task1d()
print("----------------------------- TASK e ----------------------\n")
task1e(word_list)

sc.stop()
#----------------------------------------------------------------
# Spark Streaming Twitter Trending Hashtags

Demo project from pluralsight course [Getting Started with Stream Processing with Spark Streaming](https://app.pluralsight.com/library/courses/spark-streaming-stream-processing-getting-started/table-of-contents). To run this demo you need to follow the instructions:

 - Install [Apache Spark](https://spark.apache.org/docs/latest/). 
 - Insert your Twitter API credentials in `secret.json` file. 
 - Run the following commands:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python twitter_socket.py
$ spark-submit twitter_stream.py
```
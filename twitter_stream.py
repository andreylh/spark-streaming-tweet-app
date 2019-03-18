#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from pyspark import (SparkContext, SparkConf)
from pyspark.streaming import StreamingContext

if __name__ == '__main__':

    sc = SparkContext(appName='StreamingWordCount')
    ssc = StreamingContext(sc, 2)

    ssc.checkpoint('file:///tmp/spark')

    lines = ssc.socketTextStream('localhost', 7777)

    def countWords(newValues, lastSum):
        if lastSum is None:
            lastSum = 0
        return sum(newValues, lastSum)  

    word_counts = lines.flatMap(lambda line: line.split(' '))\
                  .filter(lambda w: w != '#' and w.startswith('#'))\
                  .map(lambda word: (word, 1))\
                  .updateStateByKey(countWords)

    # Ordena pelas hashtags mais comentadas
    sorted_ = word_counts.transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False))

    sorted_.pprint(10)

    ssc.start()
    ssc.awaitTermination()
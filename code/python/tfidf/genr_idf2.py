
from __future__ import division

import jieba
import jieba.analyse
import psu


import math
from textblob import TextBlob as tb


import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

def tf(word, blob):
    return blob.words_count[word] / blob.words_len

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words_count)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def build_words_count(blob):
    words_count = {}
    for word in blob.words:
        if words_count.get(word):
            words_count[word] += 1
        else:
            words_count[word] = 1

    return words_count

files = psu.ls()

files = filter(lambda x: x.endswith('txt'), files)

data = []
for file in files:
    with open (file, "r") as myfile:
        d=myfile.read().replace('\n', '')
        d = unicode(d, errors='ignore')
        data.append(tb(d))

bloblist = data

print('for blob')
for blob in bloblist:
    print(len(blob.words))
    blob.words_count = build_words_count(blob)
    blob.words_len = len(blob.words)

for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    #import pdb;pdb.set_trace()
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:30]:
        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))



import pdb;pdb.set_trace()


print('exit')



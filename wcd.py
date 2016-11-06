import csv
import gensim
import numpy
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from nltk.corpus import stopwords
stop = stopwords.words('english')

model = gensim.models.Word2Vec.load_word2vec_format(
    'GoogleNews-vectors-negative300.bin', binary=True)
reader = csv.reader(open('filtered_data.csv'),
                    delimiter='\t', quoting=csv.QUOTE_NONE)
dict_data = {}


def clean_query(query):
    query = query.lower()  # converted to lowercase alphabet
    query = tokenizer.tokenize(query)  # tokenized
    query = [q for q in query if q not in stop]  # removed stop words
    return query


def wordvec(word):
    try:
        return model[word]
    except KeyError:
        pass
    return None


def get_centroid(query):
    query = clean_query(query)
    s = numpy.zeros(len(model["one"]))  # just a hack
    length = 0
    for a in query:
        if (a in model):
            s += model[a]
            length += 1
    if (length == 0):
        return s
    s = s / length
    return s

for line in reader:
    dict_data[line[0]] = line[1:]

TITLE = 0
AUTHORS = 1
YEAR = 2
VENUE = 3
ABSTRACT = 4
REFS = 5

# Get the Word Centroid Difference

def get_knn_wcd(query_id, num):
    dic={}
    vec_A = get_centroid(dict_data[query_id][ABSTRACT])
    for i in dict_data:
        if (i == query_id):
            continue
        vec_B = get_centroid(dict_data[i][ABSTRACT])
        val = numpy.linalg.norm(vec_A - vec_B)
        if(len(dic)<num):
            dic[i]=val
        else:
            m=max(dic,key=dic.get)
            if(dic[m]>val):
                del (dic[m])
                dic[i]=val
    return list(dic.keys())

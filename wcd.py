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
    dict_data[line[0]].append(get_centroid(line[5]))  # line[5] is abstract

TITLE = 0
AUTHORS = 1
YEAR = 2
VENUE = 3
ABSTRACT = 4
REFS = 5
CENTROID = 6

# Get the Word Centroid Difference


def wcd(id1, id2):
    # returns the norm of the difference of the two vectors
    return numpy.linalg.norm(dict_data[id1][CENTROID] - dict_data[id2][CENTROID])

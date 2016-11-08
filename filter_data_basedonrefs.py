import csv

reader = csv.reader(open('filtered_data.csv'),
                    delimiter='\t', quoting=csv.QUOTE_NONE)
dict_data = {}

for line in reader:
    dict_data[line[0]] = line[1:]
    dict_data[line[0]][5] = set(eval(dict_data[line[0]][5]))


TITLE = 0
AUTHORS = 1
YEAR = 2
VENUE = 3
ABSTRACT = 4
REFS = 5

backup_dict = set(dict_data)
def filter_ref(item):
    return item in backup_dict

i = 0
for a in backup_dict:
    i += 1
    print (i)
    dict_data[a][REFS] = set(filter(filter_ref, dict_data[a][REFS]))

i = 0
for a in backup_dict:
    i += 1
    print (i)
    for b in dict_data[a][REFS]:
        dict_data[b][REFS].add(a)


count = {}
for a in range(10000):
    count[a] = 0

for a in dict_data:
    count[len(dict_data[a][REFS])] += 1

import json
with open('count_data_init.txt', 'w') as outfile:
     json.dump(count, outfile, sort_keys = True, indent = 4,
ensure_ascii=False)


total_removed = 0
for a in backup_dict:
    if len(dict_data[a][REFS]) <= 5:
        total_removed += 1
        del dict_data[a]


backup_dict_n = set(dict_data)

def filter_ref(item):
    return item in backup_dict_n

i = 0
for a in backup_dict_n:
    i += 1
    print (i)
    dict_data[a][REFS] = set(filter(filter_ref, dict_data[a][REFS]))


count = {}
for a in range(10000):
    count[a] = 0

for a in dict_data:
    count[len(dict_data[a][REFS])] += 1

import json
with open('count_data_final.txt', 'w') as outfile:
     json.dump(count, outfile, sort_keys = True, indent = 4,
ensure_ascii=False)

total_removed = 0
for a in backup_dict_n:
    if len(dict_data[a][REFS]) == 0:
        total_removed += 1
        del dict_data[a]

dict_data_back = dict_data

f1 = open('filtered_data_small.csv', 'wb')
for a in dict_data:
    to_write = ''
    to_write += a + '\t'
    for b in dict_data[a]:
        to_write += str(b) + '\t'
    to_write += '\n'
    f1.write(to_write.encode("utf-8"))

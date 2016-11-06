# Filters the data, the csv file consists of only those enries which have abstract
# separated by tabs

import json
import re

title_pattern = re.compile("#\*([^\r\n]*)")
author_pattern = re.compile("#@([^\r\n]*)")
affiliations_pattern = re.compile("#o([^\r\n]*)")
year_pattern = re.compile("#t ([0-9]*)")
venue_pattern = re.compile("#c([^\r\n]*)")
id_pattern = re.compile("#index([^\r\n]*)")
refs_pattern = re.compile("#%([^\r\n]*)")
abstract_pattern = re.compile("#!([^\r\n]*)")


def match(line, pattern):
    """Return first group of match on line for pattern."""
    m = pattern.match(line)
    return m.groups()[0].decode('utf-8').strip() if m else None
    # return m.groups()[0] if m else None


def fmatch(f, pattern):
    """Call `match` on the next line of the file."""
    return match(f.readline(), pattern)


f = open('AMiner-Paper.txt', 'r')
# data = f.readlines()

dict_data = {}
total_count = 0
no_abstract = 0
no_title = 0
no_refs = 0
no_authors = 0
no_year = 0
no_venue = 0

f1 = open('filtered_data.csv', 'w')
while (f):
    paperid = fmatch(f, id_pattern)
    title = fmatch(f, title_pattern)
    if title is None:
        break
    total_count += 1
    authors = fmatch(f, author_pattern)
    dump = f.readline()  # discard affiliation info
    year = fmatch(f, year_pattern)
    venue = fmatch(f, venue_pattern)
    # read out reference list
    refs = []
    line = f.readline()
    m = match(line, refs_pattern)
    while m is not None:
        if m:
            refs.append(m)
        line = f.readline()
        m = match(line, refs_pattern)
    abstract = match(line, abstract_pattern)
    if (abstract == None):
        continue
    no_abstract += 1
    if (not len(refs) == 0):
        no_refs += 1
    if (not title == None):
        no_title += 1
    if (not authors == None):
        no_authors += 1
    if (not year == None):
        no_year += 1
    if (not venue == None):
        no_venue += 1
    print(no_abstract, total_count)
    if line.strip():
        f.readline()  # consume blank line
    records = paperid + '\t' + title + '\t' + authors + '\t' + \
        year + '\t' + venue + '\t' + abstract + '\t'
    if len(refs) == 0:
        records += 'NONE' + '\n'
    else:
        records += refs[0]
        for a in refs[1:]:
            records += ', ' + a
        records += '\n'
    f1.write(records.encode("utf-8"))

#!/usr/bin/env python
# g1luongg
# 996268275
import sys
sys.path.append('/u/csc2501h/include/a4')
from Asst4 import nyt_big, nyt_mini, DefaultNpPattern
# nyt_big  is the full POS-tagged 2004 NY Times corpus.
# nyt_mini is the first 100K lines of nyt_big.
# Use nyt_big for your final submission. You can use nyt_mini
# for testing and debugging your code during code development.
# DefaultNpPattern is a simple baseline pattern for NP chunking

from Asst4 import wn17 as wn
# Import version 1.7 of WordNet.
# Newer versions will not work for Question 2!

# create a chunk parser with the default pattern for NPs
from nltk.chunk.regexp import *
BaselineNpChunkRule = ChunkRule(DefaultNpPattern,
                                'Default rule for NP chunking')
NpChunker = RegexpChunkParser([BaselineNpChunkRule],
                              chunk_node='NP',top_node='S')

import re

class Hyponym(object):

    def __init__(self, hyponym, hypernym):
        self.hyponym = hyponym
        self.hypernym = hypernym
        self.confidence = 1


class Hypernym(object):

    def __init__(self, hypernym):
        self.hypernym = hypernym
        self.hyponyms = []

    def add_hyponym(self, hyponym):
        self.hyponyms.append(hyponym)


def get_confidence(num):
    if num < 0:
        return "Zero Confidence"
    elif num == 1:
        return "Low Confidence"
    elif num == 2:
        return "Medium Confidence"
    else:
        return "High Confidence"


############################################
# Hearst's patterns for discovering hyponyms

### Components to Hearst's patterns

# Return regular expression to extract the hyponym NP
def re_hyponym(query):
    res = '(?P<hyponym>' + query + ')'
    return res

# Regular expression to extract NP from the tree
re_np = '\(NP (?P<np>[^)]*)\)'

# Regular expression to extract the hypernym NP
re_hypernym = '(?P<hypernym>' + re_np + ')'

# Regular expression to match and not capture the commas
re_comma = '(?:,/,)'
# Matches optional {,}
re_comma_optional =  re_comma + '?'

# Regular expression to match and not capture {and|or}
re_and_or = '(?:and/\S+|or/\S+)?'

# Regular expression for NP_0{, NP_1, ...,}
re_np_comma = re_np + '((' + re_comma + '\s+' + re_np + ')*)?'

# Regular expression for NP_0{, NP_1, ..., {and|or} NP_j}
re_np_and_or = re_np + '((' + re_comma + '\s+' + re_np + ')*' + re_comma + \
    '\s+' + re_and_or + '(\s+)?' + re_np + ')?'


### Hearst's Patterns

# Pattern 1: NP_0{,} such as NP_1{, NP_2, ..., {and|or} NP_j}
re_hypernym_such_as_hyponym = re_hypernym + re_comma_optional + \
    '\s+such/\S+\s+as/\S+\s+' + re_hyponym(re_np_and_or)
pattern1 = re.compile(re_hypernym_such_as_hyponym)

# Pattern 2: such NP_0 as NP_1{,NP_2,..., {and|or}NP_j}
re_such_hypernym_as_hyponym = 'such/\S+\s+' + re_hypernym + '\s+as/\S+\s+' + \
    re_hyponym(re_np_and_or)
pattern2 = re.compile(re_such_hypernym_as_hyponym)

# Pattern 3: NP_0{, NP_1, ...,} {and|or} other NP_j
re_hyponym_other_hypernym = re_hyponym(re_np_comma) + '\s+' + re_and_or + \
    '(\s)?+other/\S+\s+' + re_hypernym
pattern3 = re.compile(re_hyponym_other_hypernym)

# Pattern 4: NP_0{,} including NP_1{, NP_2, ..., {and|or} NP_j}
re_hypernym_including_hyponym = re_hypernym + re_comma_optional + \
    '\s+including/\S+\s+' + re_hyponym(re_np_and_or)
pattern4 = re.compile(re_hypernym_including_hyponym)

# Pattern 5: NP_0{,} especially NP_1{, NP_2, ..., {and|or}}
re_hypernym_especially_hyponym = re_hypernym + re_comma_optional + \
    '\s+especially/\S+\s+' + re_hyponym(re_np_and_or)
pattern5 = re.compile(re_hypernym_especially_hyponym)

patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]

# just for the purpose of illustration, print the output of the
# NP Chunker for the first 3 sentences of nyt_mini
for s in nyt_mini.tagged_sents()[0:3]:
    tagged_sent = str(NpChunker.parse(s)).replace('\n', '')
    for pattern in patterns:
        matches = pattern.match(tagged_sent)
        print matches

# also just for the purpose of illustration, print the synsets
# for the word 'assignment'
for x in wn.synsets('assignment','n'):
    print x

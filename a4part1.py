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

from P1patterns import patterns

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




# just for the purpose of illustration, print the output of the
# NP Chunker for the first 3 sentences of nyt_mini
for s in nyt_mini.tagged_sents():
    try:
        tagged_sent = str(NpChunker.parse(s)).replace('\n', '')
        for pattern in patterns:
            matches = pattern.match(tagged_sent)
            if matches:
                # print tagged_sent
                print matches
    except:
        continue

# also just for the purpose of illustration, print the synsets
# for the word 'assignment'
# for x in wn.synsets('assignment','n'):
#     print x

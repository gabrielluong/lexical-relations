#!/usr/bin/env python
# g1luongg
# 996268275
import sys, re
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

from HeartPattern import patterns
# Import Hearst's patterns


def get_confidence(num):
    if num == 1:
        return "Low Confidence"
    elif num == 2:
        return "Medium Confidence"
    else:
        return "High Confidence"


# Return the NP from the tagged NP
# Example: "(NP Mr./NP Everest/NP)" => "Mr Everest"
def get_np(tagged_np):
    return "_".join(re.findall('(\S+)/\w+', tagged_np)).lower()


# Return a list of the tagged NPs in the matched group of hyponyms.
# Example:
# "(NP grease/NN)  ,/,  and/CC  (NP insect/NN pesticides/NNS)"
#   => ['(NP grease/NN)', '(NP insect/NN pesticides/NNS)']
def extract_hyponyms(match):
    return re.findall('\(NP\s+[^)]*\)', match, flags=re.IGNORECASE)


def find_hypernym_relations(sents):
    # Dictionary that keeps track of the tuple (hyponym, hypernym) pairs and
    # their occurrence count and tagged sentence
    pairs = {}

    for s in sents:
        try:
            # Get an appropriate string representation of the tree structure
            # of the tagged sentence
            tagged_sent = str(NpChunker.parse(s)).replace('\n', '')
            for pattern in patterns:
                matches = pattern.search(tagged_sent)
                if matches:
                    hypernym = get_np(matches.group('hypernym'))
                    hyponyms = extract_hyponyms(matches.group('hyponym'))

                    for hyponym in hyponyms:
                        hyponym = get_np(hyponym)
                        hyponym_pair = (hyponym, hypernym)
                        pairs.setdefault(hyponym_pair, {
                            'count': 0,
                            'sentence': []
                        })
                        pairs[hyponym_pair]['count'] += 1
                        if not tagged_sent in pairs[hyponym_pair]['sentence']:
                            pairs[hyponym_pair]['sentence'].append(tagged_sent)
        except:
            continue

    return pairs


# Dictionary for each case that contains the confidence level as a key,
# and a dictionary containing the hyponym and hypernym pair, and tagged
# sentence as the value.
case1 = {"Low Confidence": [], "Medium Confidence": [], "High Confidence": []}
case2 = {"Low Confidence": [], "Medium Confidence": [], "High Confidence": []}
case3 = {"Low Confidence": [], "Medium Confidence": [], "High Confidence": []}
case4 = {"Low Confidence": [], "Medium Confidence": [], "High Confidence": []}


# Evaluate the suggested pair for each of the cases and categorize them according
# to their confidence level
def evaluate_cases(hyp_pairs):
    for (pair, data) in hyp_pairs.items():
        hyponym = pair[0]
        hypernym = pair[1]
        count = data['count']
        sentence = data['sentence']

        if is_case1(hyponym, hypernym):
            case1[get_confidence(count)].append({
                'count': count,
                'sentence': sentence,
                'hyponym': hyponym,
                'hypernym': hypernym
            })
        if is_case2(hyponym, hypernym):
            case2[get_confidence(count)].append({
                'count': count,
                'sentence': sentence,
                'hyponym': hyponym,
                'hypernym': hypernym
            })
        if is_case3(hyponym, hypernym):
            case3[get_confidence(count)].append({
                'count': count,
                'sentence': sentence,
                'hyponym': hyponym,
                'hypernym': hypernym
            })
        if is_case4(hyponym, hypernym):
            case4[get_confidence(count)].append({
                'count': count,
                'sentence': sentence,
                'hyponym': hyponym,
                'hypernym': hypernym
            })


# List that keeps track of pairs of hyponym and hypernym that are related.
# Used as an optimization for is_sense_related()
related = []

# Return True if one or more senses of each word is related between the two
# given words, and false otherwise.
def is_sense_related(hyponym, hypernym):
    if (hyponym, hypernym) in related:
        return True

    hyponym_synsets = wn.synsets(hyponym)
    hypernym_synsets = wn.synsets(hypernym)
    result = False

    # Check that both words are present in WordNet
    if hyponym_synsets and hypernym_synsets:
        for hypernym_synset in hypernym_synsets:
            for hyponym_synset in hyponym_synsets:
                # Find all synsets that hypernyms of the hyponym synset and
                # the hypernym synset, and check if there is any relations.
                result = len(hyponym_synset.common_hypernyms(hypernym_synset)) > 0
                if result:
                    # Add the pair as a tuple to the list related
                    related.append((hyponym, hypernym))
                    break

    return result


# Return whether or not both words are present in WordNet, and a relation holds
# between the one or more senses of each.
def is_case1(hyponym, hypernym):
    return is_sense_related(hyponym, hypernym)


# Return whether or not the relation is contracted by WordNet for at least one
# sense of each word
def is_case2(hyponym, hypernym):
    return is_case1 and is_sense_related(hypernym, hyponym)


# Return whether or not both words are already in WordNet, and the relation is
# not present
def is_case3(hyponym, hypernym):
    return wn.synsets(hyponym) and wn.synsets(hypernym) and \
        not is_case1(hyponym, hypernym)


# Return whether or not one or both of the words is missing from WordNet.
def is_case4(hyponym, hypernym):
    return not wn.synsets(hyponym) or not wn.synsets(hypernym)


# Print the data in the case dictionaries.
def print_case(case_num, case, print_sentence=False):
    for i in range(1, 4):
        confidence = get_confidence(i)

        if confidence in case:
            data = case[confidence]
            print "Case", case_num, "-", confidence, "(", len(data), ")"
            print "=" * 50
            for d in data:
                if print_sentence:
                    print d['sentence']
                print "HYPONYM(%s, %s)" % (d['hyponym'], d['hypernym'])
        else:
            print "Case", case_num, "-", confidence, "(0)"
        print "\n" * 2


if __name__ == "__main__":
    hyp_pair_dict = find_hypernym_relations(nyt_big.tagged_sents())
    # hyp_pair_dict = find_hypernym_relations(nyt_mini.tagged_sents())
    evaluate_cases(hyp_pair_dict)

    print_case(1, case1)
    print_case(2, case2)
    print_case(3, case3)
    print_case(4, case4)

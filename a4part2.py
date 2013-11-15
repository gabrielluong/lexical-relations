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

from P2patterns import pattern
# Import Girju's patterns


# Return a list of the causal verbs
def get_causal_verbs():
    lines = [line.strip() for line in open('Causal-verbs.txt')]

    for i in range(len(lines)):
        words = lines[i].split(" ")
        # Check if the last word for the line matches an optional preposition.
        # If so, remove it from the newly joined word.
        if re.match('\(\w+\)', words[-1], flags=re.IGNORECASE):
            words.pop(-1)
        lines[i] = "_".join(words)

    return lines


# Return the word from the tagged component
# Example: (NP Mr/NP Everest/NP)"" => "Mr_Everest"
def get_word(tagged_component):
    return "_".join(re.findall('(\S+)/\w+', tagged_component)).lower()


def find_casual_relations(sents):
    # Dictionary that keeps track of the tuple (hyponym, hypernym) pairs and
    # their occurrence count and tagged sentence
    result = []
    casual_verbs = get_causal_verbs()

    for s in sents:
        try:
            # Get an appropriate string representation of the tree structure
            # of the tagged sentence
            tagged_sent = str(NpChunker.parse(s)).replace('\n', '')
            matches = pattern.search(tagged_sent)
            if matches:
                np1 = get_word(matches.group('NP1'))
                np2 = get_word(matches.group('NP2'))
                verb = get_word(matches.group('verb'))
                preposition = get_word(matches.group('preposition'))

                if verb in causal_verbs and \
                    is_causal(np1, np2, verb, preposition):
                    result.append({
                        'NP1': np1,
                        'NP2': np2,
                        'verb': verb,
                        'preposition': preposition
                    })
        except:
            continue

    return result


# Returns True if the given NP1-verb-NP2 indicates a casual relations, and false
# otherwise.
def is_causal(np1, np2, verb, preposition):
    result = False

    if not is_non_causal_relations(np1, np2, verb, preposition):
        if re.match('^cause[ds]?$', verb, flags=re.IGNORECASE):
            result = True
        elif is_hyponym(np2, 'phenomenon.n.01'):
            result = True
        elif re.match('^associate[d]?$', verb, flags=re.IGNORECASE) and \
            preposition == 'with' and not is_hyponym(np1, 'entity.n.01') and \
            not is_hyponym(np2, 'abstraction.n.06') and \
            not is_hyponym(np2, 'group.n.01') and \
            not is_hyponym(np2, 'possession.n.02'):
            result = True
        elif re.match('^relate[d]?$', verb, flags=re.IGNORECASE) and \
            preposition == 'to' and \
            not is_hyponym(np1, 'entity.n.01') and \
            not is_hyponym(np2, 'abstraction.n.06') and \
            not is_hyponym(np2, 'group.n.01') and \
            not is_hyponym(np2, 'possession.n.02'):
            result = True
        elif not is_hyponym(np1, 'entity.n.01') and is_hyponym(np2, 'event.n.01'):
            result = True
        elif not is_hyponym(np1, 'abstraction.n.06') and \
            (is_hyponym(np2, 'event.n.01') or is_hyponym(np2, 'act.n.02')):
            result = True
        elif re.match('^lead$', verb, flags=re.IGNORECASE) and \
            preposition == 'to' and \
            not is_hyponym(np2, 'entity.n.01') and \
            not is_hyponym(np2, 'group.n.01'):
            result = True

    return result


# Returns True if the given NP1-verb-NP2 indicates a non-casual relations, and
# false otherwise.
def is_non_causal_relations(np1, np2, verb, preposition):
    result = False

    if re.match('^induce[ds]?$', verb, flags=re.IGNORECASE) and \
        (is_hyponym(np2, 'entity.n.01') or is_hyponym(np2, 'abstraction.n.06')):
        result = True
    elif is_hyponym(np2, 'group.n.01') and not is_hyponym(np2, 'state.n.04') and \
        not is_hyponym(np2, 'event.n.01') and not is_hyponym(np2, 'act.n.02'):
        result = True
    elif is_hyponym(np1, 'entity.n.01') and not is_hyponym(np2, 'state.n.04') and \
        not is_hyponym(np2, 'event.n.01') and not is_hyponym(np2, 'phenomenon.n.01'):
        result = True

    return result


# List that keeps track of pairs of hyponym and hypernym that are related.
# Used as an optimization for is_sense_related()
related = []


# Returns True if the given word is a hyponym of the root synset specified,
# and false otherwise.
def is_hyponym(word, root):
    if (word, root) in related:
        return True

    word_synsets = wn.synsets(hyponym)
    root = wn.synset(root)
    result = False

    # Check that both words are present in WordNet
    if word_synsets and root:
        for word_synset in word_synsets:
            # Find all synsets that hypernyms of the hyponym synset and
            # the hypernym synset, and check if there is any relations.
            result = len(word_synset.common_hypernyms(root)) > 0
            if result:
                # Add the pair as a tuple to the list related
                related.objectppend((word, root))
                break

    return result


# Print the data in the list of casual relations
def print_result(casual_relations, print_sentence=False):
    for relation in casual_relations:
        print '%s-%s-%s-%s' % (relation['NP1'], relation['verb'], \
            relation['preposition'], relation['NP2'])


if __name__ == "__main__":
    # casual_relations = find_casual_relations(nyt_big.tagged_sents())
    casual_relations = find_casual_relations(nyt_mini.tagged_sents())
    print_result(casual_relations)

""" 

Components that you need for for Assignment 4 in CSC2501/485, Fall 2010.

Usage:

from Asst4 import nyt_big  ## the full NYT corpus for A4
from Asst4 import nyt_mini ## only the first 100K lines from nyt_big, for 
                           ## development 
from Asst4 import wn17     ## WordNet 1.7, newer versions won't work for Q2

from Asst4 import DefaultNpChunker ## a simple NP chunker to get things started

"""

# T(he original version of t)his code was written by Ulrich Germann (11/2010)
# It provides components necessary for Assignment 4 of CSC 485/2501h

######################################################################
#
# ATTENTION! 
#
# THE INFORMATION BELOW IS ***CRUCIAL*** FOR YOUR SUCCESS IN Q2
#
# Question 2 of A4 works only with Wordnet 1.7 or earlier
# 
# QUESTION 2 WILL NOT WORK WITH THE NLTK DEFAULT WORDNET INSTALLATION!
# 
# We have installed version 1.7 in the following location
# /u/csc2501h/include/a4/nltk/corpora
# 
# To use it we need to prepend the following directory to the 
# NLTK search path for corpora and other data
import nltk
nltk.data.path[0:0] = ['/u/csc2501h/include/a4/nltk']

# Now we can import wordnet 1.7 instead of later versions 
from nltk.corpus import wordnet as wn17

# The following code provides access to the tagged NY Times corpus
# nyt_big is the full corpus
# nyt_mini a small subset for development
from nltk.data         import ZipFilePathPointer
from nltk.corpus       import TaggedCorpusReader

nyt_zipped = ZipFilePathPointer('/u/csc2501h/include/a4/nltk/corpora/nyt.zip')
nyt_big    = TaggedCorpusReader(nyt_zipped,'nyt/2004-tagged.txt',sep='/')
nyt_mini   = TaggedCorpusReader(nyt_zipped,'nyt/nytimes-mini.txt',sep='/')

# Finally, let's set up a default pattern for NP chunking
# Setting up the NP chunker itself is left to the main script, to encourage
# trying different variants of the pattern

DefaultNpPattern = ''.join([r'(<DT|AT>?<RB>?)?',
			    r'<JJ.*|CD.*>*',
			    r'(<JJ.*|CD.*><,>)*',
			    r'(<N.*>)+'])

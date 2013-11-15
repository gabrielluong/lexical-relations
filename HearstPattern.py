# g1luongg
# 996268275
import re

##### Regular expression of Hearst's patterns for discovering hyponyms

### Regular expression components to Hearst's patterns

# Returns a regular expression to extract the hyponym NP from the given query
def re_hyponym(query):
    res = '(?P<hyponym>' + query + ')\s*'
    return res

# Returns a regular expression to extract the hypernym NP from the given query
def re_hypernym(query):
    res = '(?P<hypernym>' + query + ')\s*'
    return res

# Regular expression to extract NP from the tree
re_np = '\(NP[^)]*\)'

# Regular express to extract the hypernym NP from 'other NP'
re_np_other = '\(NP\s+other/\w+\s+' + re_hypernym('[^)]*') + '\)'

# Regular expression to match and not capture the commas
re_comma = '(?:,/,\s+)'
# Matches optional {,}
re_comma_optional =  re_comma + '?'

# Regular expression to match and not capture {and|or}
re_and_or = '(?:and/\w+|or/\w+)?'

# Regular expression for NP_0{, NP_1, ...,}
re_np_comma = re_np + '\s*((' + re_comma + re_np + '\s+)*)?'

# Regular expression for NP_0{, NP_1, ..., {and|or} NP_j}
re_np_and_or = re_np + '\s*((' + re_comma + re_np + '\s+)*' + \
    re_comma_optional + re_and_or + '\s+' + re_np + ')?'


### Regular expression of Hearst's patterns

# Pattern 1: NP_0{,} such as NP_1{, NP_2, ..., {and|or} NP_j}
# \(NP[^)]*\)\s*(?:,/,\s+)?such/\w+\s+as/\w+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\w+|or/\w+)?\s+\(NP[^)]*\))?\s*
re_hypernym_such_as_hyponym = re_hypernym(re_np) + re_comma_optional + \
    'such/\w+\s+as/\w+\s+' + re_hyponym(re_np_and_or)
pattern1 = re.compile(re_hypernym_such_as_hyponym, flags=re.IGNORECASE)

# Pattern 2: such NP_0 as NP_1{,NP_2,..., {and|or}NP_j}
# such/\w+\s+\(NP[^)]*\)\s*as/\w+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\w+|or/\w+)?\s+\(NP[^)]*\))?\s*
re_such_hypernym_as_hyponym = 'such/\w+\s+' + re_hypernym(re_np) + 'as/\w+\s+' + \
    re_hyponym(re_np_and_or)
pattern2 = re.compile(re_such_hypernym_as_hyponym, flags=re.IGNORECASE)

# Pattern 3: NP_0{, NP_1, ...,} {and|or} other NP_j
# \(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*)?\s*(?:and/\w+|or/\w+)?\s*\(NP\s+other/\w+\s+[^)]*\s*\)
re_hyponym_other_hypernym = re_hyponym(re_np_comma) + re_and_or + \
    '\s*' + re_np_other
pattern3 = re.compile(re_hyponym_other_hypernym, flags=re.IGNORECASE)

# Pattern 4: NP_0{,} including NP_1{, NP_2, ..., {and|or} NP_j}
# \(NP[^)]*\)\s*(?:,/,\s+)?\s*including/\w+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\w+|or/\w+)?\s+\(NP[^)]*\))?\s*
re_hypernym_including_hyponym = re_hypernym(re_np) + re_comma_optional + \
    '\s*including/\w+\s+' + re_hyponym(re_np_and_or)
pattern4 = re.compile(re_hypernym_including_hyponym, flags=re.IGNORECASE)

# Pattern 5: NP_0{,} especially NP_1{, NP_2, ..., {and|or}}
# \(NP[^)]*\)\s*(?:,/,\s+)?\s*especially/\w+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\w+|or/\w+)?\s+\(NP[^)]*\))?\s*
re_hypernym_especially_hyponym = re_hypernym(re_np) + re_comma_optional + \
    '\s*especially/\w+\s+' + re_hyponym(re_np_and_or)
pattern5 = re.compile(re_hypernym_especially_hyponym, flags=re.IGNORECASE)

patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]

if __name__ == "__main__":
    print re_hypernym_such_as_hyponym
    print re_such_hypernym_as_hyponym
    print re_hyponym_other_hypernym
    print re_hypernym_including_hyponym
    print re_hypernym_especially_hyponym
    print
    # Sample test to extract the hyponym and hypernym from an example sentence
    # for pattern 1
    s = "(S  With/IN  current/JJ  manufactured/VBN  (NP drainage/NN systems/NNS)  ,/,  (NP pollutants/NNS)  such/JJ  as/IN  (NP grease/NN)  ,/,  (NP fertilizers/NNS)  and/CC  (NP insect/NN pesticides/NNS)  make/VBP  their/PP$  (NP way/NN)  into/IN  (NP streams/NNS)  and/CC  (NP rivers/NNS)  ./SENT)"
    other = "(NP Mr./NP Everest/NP)  and/CC  (NP other/JJ small-business/NN owners/NNS)"
    matches = pattern1.match(s)
    if matches:
        hypernym = matches.group('hypernym')
        hyponym = matches.group('hyponym')
        matches = re.findall('\(NP\s+[^)]*\)', hyponym, flags=re.IGNORECASE)
        print hypernym
        print matches
        print
    matches = pattern3.match(other)
    if matches:
        hypernym = matches.group('hypernym')
        hyponym = matches.group('hyponym')
        print hyponym
        matches = re.findall('(\S+)/\w+', "(NP Mr/NP Everest/NP)", flags=re.IGNORECASE)
        print hypernym
        print matches

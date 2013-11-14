# g1luongg
# 996268275
import re

##### Hearst's patterns for discovering hyponyms

### Components to Hearst's patterns

# Return regular expression to extract the hyponym NP
def re_hyponym(query):
    res = '(?P<hyponym>' + query + ')'
    return res

# Regular expression to extract NP from the tree
re_np = '\(NP[^)]*\)'

# Regular expression to extract the hypernym NP
re_hypernym = '(?P<hypernym>' + re_np + ')\s*'

# Regular expression to match and not capture the commas
re_comma = '(?:,/,\s+)'
# Matches optional {,}
re_comma_optional =  re_comma + '?'

# Regular expression to match and not capture {and|or}
re_and_or = '(?:and/\S+|or/\S+)?'

# Regular expression for NP_0{, NP_1, ...,}
re_np_comma = re_np + '\s*((' + re_comma + re_np + '\s+)*)?'

# Regular expression for NP_0{, NP_1, ..., {and|or} NP_j}
re_np_and_or = re_np + '\s*((' + re_comma + re_np + '\s+)*' + \
    re_comma_optional + re_and_or + '\s+' + re_np + ')?'


### Hearst's Patterns

# Pattern 1: NP_0{,} such as NP_1{, NP_2, ..., {and|or} NP_j}
# \(NP[^)]*\)\s*(?:,/,\s+)?such/\S+\s+as/\S+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?
# (?P<hypernym>\(NP[^)]*\))\s*(?:,/,\s+)?such/\S+\s+as/\S+\s+(?P<hyponym>\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?)
re_hypernym_such_as_hyponym = re_hypernym + re_comma_optional + \
    'such/\S+\s+as/\S+\s+' + re_hyponym(re_np_and_or)
pattern1 = re.compile(re_hypernym_such_as_hyponym, flags=re.IGNORECASE)

# Pattern 2: such NP_0 as NP_1{,NP_2,..., {and|or}NP_j}
# such/\S+\s+\(NP[^)]*\)\s*as/\S+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?
# such/\S+\s+(?P<hypernym>\(NP[^)]*\))\s*as/\S+\s+(?P<hyponym>\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?)
re_such_hypernym_as_hyponym = 'such/\S+\s+' + re_hypernym + 'as/\S+\s+' + \
    re_hyponym(re_np_and_or)
pattern2 = re.compile(re_such_hypernym_as_hyponym, flags=re.IGNORECASE)

# Pattern 3: NP_0{, NP_1, ...,} {and|or} other NP_j
# \(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*)?\s*(?:and/\S+|or/\S+)?\s*other/\S+\s+\(NP[^)]*\)\s*
# (?P<hyponym>\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*)?)\s*(?:and/\S+|or/\S+)?\s*other/\S+\s+(?P<hypernym>\(NP[^)]*\))\s*
re_hyponym_other_hypernym = re_hyponym(re_np_comma) + '\s*' + re_and_or + \
    '\s*other/\S+\s+' + re_hypernym
pattern3 = re.compile(re_hyponym_other_hypernym, flags=re.IGNORECASE)

# Pattern 4: NP_0{,} including NP_1{, NP_2, ..., {and|or} NP_j}
# \(NP[^)]*\)\s*(?:,/,\s+)?\s*including/\S+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?
# (?P<hypernym>\(NP[^)]*\))\s*(?:,/,\s+)?\s*including/\S+\s+(?P<hyponym>\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?)
re_hypernym_including_hyponym = re_hypernym + re_comma_optional + \
    '\s*including/\S+\s+' + re_hyponym(re_np_and_or)
pattern4 = re.compile(re_hypernym_including_hyponym, flags=re.IGNORECASE)

# Pattern 5: NP_0{,} especially NP_1{, NP_2, ..., {and|or}}
# \(NP[^)]*\)\s*(?:,/,\s+)?\s*especially/\S+\s+\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?
# (?P<hypernym>\(NP[^)]*\))\s*(?:,/,\s+)?\s*especially/\S+\s+(?P<hyponym>\(NP[^)]*\)\s*(((?:,/,\s+)\(NP[^)]*\)\s+)*(?:,/,\s+)?(?:and/\S+|or/\S+)?\s+\(NP[^)]*\))?)
re_hypernym_especially_hyponym = re_hypernym + re_comma_optional + \
    '\s*especially/\S+\s+' + re_hyponym(re_np_and_or)
pattern5 = re.compile(re_hypernym_especially_hyponym, flags=re.IGNORECASE)

patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]


if __name__ == "__main__":
    print re_hypernym_such_as_hyponym
    print re_such_hypernym_as_hyponym
    print re_hyponym_other_hypernym
    print re_hypernym_including_hyponym
    print re_hypernym_especially_hyponym

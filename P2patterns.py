# g1luongg
# 996268275
import re

##### Regular expression of Girju's patterns

### Regular expression components to Girju's patterns

# Regular expression to extract NP
re_np = '\(NP[^)]*\)'

# Regular expression for a verb: <verb>/V<pos>
re_verb = '(?P<verb>\w+/V\w*)\s*'

# Regular expression to extract the preposition {to|with|from|in}
re_to_with_from_in = '(P<preposition>to/\w+|with/\w+|from/\w+|in/\w+)?\s*'


### Regular expression of Girju's patterns
# \(NP[^)]*\)\s*\w+/V\w*\s*(to/\w+|with/\w+|from/\w+|in/\w+)?\s*\(NP[^)]*\)
re_girju = '(?P<NP1>' + re_np + ')\s*' + re_verb + re_to_with_from_in + \
    '(?P<NP2>' + re_np + ')'
pattern = re.compile(re_girju)


if __name__ == "__main__":
    print re_girju

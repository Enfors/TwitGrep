#!/usr/bin/env python3

"""Search Twitter for specified words in real time. Output as csv.
"""

import twitgrep
import text

SEARCH_TERMS=["#svpol"]

try:
    for status in twitgrep.TwitGrep(SEARCH_TERMS):
        for sentence in text.normalize_and_split_sentences(status.text):
            print(sentence)
except KeyboardInterrupt:
    print()
    raise SystemExit

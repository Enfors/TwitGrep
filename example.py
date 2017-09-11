#!/usr/bin/env python3
"Example file illustrating how to use twitgrep from another program."

import twitgrep

SEARCH_TERMS=["python", "#svpol", "emacs"]

print("Streaming search results for search terms: " + str(SEARCH_TERMS))

for status in twitgrep.TwitGrep(SEARCH_TERMS):
    print("----------------------------\nTweet from user '%s':\n%s" % \
          (status.user.screen_name, status.text))

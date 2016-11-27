#!/usr/bin/env python2.7
"Example file illustrating how to use twitgrep from another program."

from __future__ import print_function

import twitgrep

for status in twitgrep.TwitGrep(["python", "#svpol", "emacs"]):
    print("----------------------------\nTweet from user '%s':\n%s" % \
          (status.user.screen_name, status.text))

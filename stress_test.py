#!/usr/bin/env python2.7
"Example file illustrating how to use twitgrep from another program."

from __future__ import print_function

import sys
import time

import twitgrep

num_total = 0

start_time = int(time.time())
duration = 60 
end_time = start_time + duration

now = start_time

for status in twitgrep.TwitGrep(["python", "#svpol", "and"]):
    num_total = num_total + 1
    if int(time.time()) == now:
        sys.stdout.write(".")
    else:
        now = int(time.time())
        sys.stdout.write("o")
    sys.stdout.flush()
    if time.time() >= end_time:
        print("\nTotal: %d, %d per second." % (num_total, num_total / duration))
        raise SystemExit

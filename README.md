# TwitGrep

TwitGrep provies a tool for searching Twitter for a list of specific
words in real time. It also aims to provide tools for analyzing the
tweets found.

## Overview

This is an overview of the functionality provided. For more information,
please refer to the docstrings in each file.

### twitgrep.py

This file provides the ``TwitGrep`` class, which performs the actual
Twitter searching. The class is implemented as an iterator, making it
simple to step through the search results.

### example.py

This file shows how to use the ``TwitGrep`` class from another program
to search Twitter in real time.

### stress_test.py

This script is another example of how to use the ``TwitGrep`` class,
but this time with very generic and common search words, to provide
as many results as possible. It turns out that Twitter limits us to
no more than 50-ish results per second. ``stress_test.py``
illustrates this.

### text.py

The previous files all dealt with getting data from Twitter. Now we've
eached the analysis functionality that we can apply to that data. The
``text.py`` file defines classes like ``Word`` and ``Sentence``.

### ngram.py

This file provides the ``NGram`` and ``ValueNGram`` classes, that we
can use to create bi-grams, 3-grams, 4-grams etc, for detailed
analysis.

### normalize.py

This file contains classes that make it possible to "normalize" text;
that is, divide text into sentences, remove punctuation, and whatnot.



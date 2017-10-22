#!/usr/bin/env python3

"""Create and use n-grams (bigrams, 2-grams, 3-grams, etc)
"""

import doctest


class NGram(object):
    """The ngram class stores an n-gram.

    Given a list of words, an n-gram is created. If a list of two words
    is provided, a bi-gram is created. If three words are provided, a
    3-gram is created, and so on.

    >>> word1 = Word("some")
    >>> word2 = Word("words")
    >>> bi_gram = NGram([word1, word2])
    >>> bi_gram
    NGram(['some', 'words'])
    >>> print(bi_gram)
    two words
    >>> len(bi_gram)
    2
    """

    def __init__(self, words):
        if not words:
            words = []
        else:
            self.words = words

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return "NGram(%s)" % self.words

    def __str__(self):
        output = ""

        for word in self.words:
            output = output + str(word) + " "

        return output.strip()


class ValueNGram(NGram):
    """A ValueNGram is an NGram with a value. Can be used for sentiment
    analysis, and the like.

    >>> value_bi_gram = ValueNGram(["some", "words"], value=3)
    >>> value_bi_gram
    ValueNGram(['some', 'words'], value=3)
    >>> print(value_bi_gram)
    some words: 3
    """

    def __init__(self, words, value=0):
        super().__init__(words)
        self.value = value

    def __repr__(self):
        return "ValueNGram(%s, value=%d)" % (self.words, self.value)

    def __str__(self):
        return super().__str__() + ": %d" % self.value


if __name__ == "__main__":
    doctest.testmod()

#!/usr/bin/env python3

"""doctest demo

>>> bag = BagOfWords("A lot of silly little words".split(" "))
>>> bag
BagOfWords(['a', 'lot', 'of', 'silly', 'little', 'words'])
"""

class BagOfWords(object):
    """Represents a bag of words.

    All words in the bag are automatically made lowercase.

    How to make a bag:

    >>> bag = BagOfWords(["A", "bunch", "of", "words"])
    >>> bag
    BagOfWords(['a', 'bunch', 'of', 'words'])

    You can add more words to an existing bag:

    >>> bag.add_words(["Some", "more", "words"])
    >>> bag
    BagOfWords(['a', 'bunch', 'of', 'words', 'some', 'more'])
    >>> len(bag)
    6

    You can also generate a frequency vector:

    >>> bag.gen_frequency_vec(["some", "words"])
    [0, 0, 0, 1, 1, 0]
    >>> bag.gen_frequency_vec(["some", "more", "words"])
    [0, 0, 0, 1, 1, 1]
    """

    def __init__(self, words=None):
        """Instanciate a bag.

        >>> bag = BagOfWords(["some", "words"])
        >>> bag
        BagOfWords(['some', 'words'])
        """
        self.words = []
        if words is not None:
            self.add_words(words)

    def add_words(self, words):
        """Add words to the bag.

        >>> bag = BagOfWords("some silly old words".split(" "))
        >>> bag
        BagOfWords(['some', 'silly', 'old', 'words'])
        >>> len(bag)
        4
        >>> bag.add_words("more words".split(" "))
        >>> bag
        BagOfWords(['some', 'silly', 'old', 'words', 'more'])
        >>> len(bag)
        5
        """
        for word in words:
            word = word.lower()
            if word not in self.words:
                self.words.append(word)

    def gen_frequency_vec(self, in_words):
        """Return a frequency vector for in_words.
        >>> bag = BagOfWords("A lot of silly little words of little meaning".split(" "))
        >>> bag
        BagOfWords(['a', 'lot', 'of', 'silly', 'little', 'words', 'meaning'])
        >>> bag.gen_frequency_vec("some silly words".split(" "))
        [0, 0, 0, 1, 0, 1, 0]
        """
        frequency_vec = []

        for word in self.words:
            frequency_vec.append(in_words.count(word.lower()))

        return frequency_vec


    def __str__(self):
        """Return a human-readable string representing the bag.

        >>> bag = BagOfWords("some silly words".split(" "))
        >>> str(bag)
        "['some', 'silly', 'words']"

        This function is implicitly used when printing a bag:

        >>> print(bag)
        ['some', 'silly', 'words']
        """
        return str(self.words)

    def __repr__(self):
        """Return the code needed to create this bag.

        >>> bag = BagOfWords("some silly words".split(" "))
        >>> bag
        BagOfWords(['some', 'silly', 'words'])
        """
        return "BagOfWords(%s)" % self.words

    def __len__(self):
        """Return the number of words in the bag.

        >>> bag = BagOfWords("some silly words".split(" "))
        >>> bag
        BagOfWords(['some', 'silly', 'words'])
        >>> len(bag)
        3
        >>> bag.add_words("more words".split(" "))
        >>> len(bag)
        4
        """
        return len(self.words)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

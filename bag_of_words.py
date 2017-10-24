#!/usr/bin/env python3

"""record the frequency of word occurance
"""


class BagOfWords(object):
    """Represents a bag of words.

    All words in the bag are automatically made lowercase.

    How to make a bag:

    >>> bag = BagOfWords(["A", "bunch", "of", "words"])

    You can add more words to an existing bag:

    >>> bag.add_words(["Some", "more", "words"])
    >>> len(bag)
    6
    """

    def __init__(self, words=None):
        """Instanciate a bag.
        """
        self.words = {}
        if words is not None:
            self.add_words(words)

    def add_words(self, words):
        """Add words to the bag.

        >>> bag = BagOfWords("some silly old words".split(" "))
        >>> len(bag)
        4
        >>> bag.add_words("more words".split(" "))
        >>> len(bag)
        5
        """
        for word in words:
            try:
                num = self.words[word]
            except KeyError:
                num = 0

            num = num + 1
            self.words[word] = num

    def sorted_matrix(self, reverse=False):
        """Return a matrix with words and frequencies, sorted by
        frequency (descending).
        >>> bag = BagOfWords("some silly words".split(" "))
        >>> bag.add_words("some silly".split(" "))
        >>> bag.add_words(["some"])
        >>> for k, v in bag.sorted_matrix():
        ...     print(k, v)
        words 1
        silly 2
        some 3
        """

        matrix = [(k, self.words[k]) for k in sorted(self.words,
                                                     key=self.words.get,
                                                     reverse=reverse)]
        return matrix

    def __str__(self):
        """Return a human-readable string representing the bag.
        """
        return str(self.words)

    def __repr__(self):
        """Return the code needed to create this bag.
        """
        return "BagOfWords(%s)" % self.words()

    def __len__(self):
        """Return the number of words in the bag.

        >>> bag = BagOfWords("some silly words".split(" "))
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

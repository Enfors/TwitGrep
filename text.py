#!/usr/bin/env python3

"""Classes for words and sentences.
"""

import doctest


class Word(object):
    """Store a word along with it's type.

    We create a word like this:

    >>> word = Word("fnurgle", word_type=Word.TYPE_WORD)
    >>> word
    Word('fnurgle', word_type=1)
    >>> print(word)
    fnurgle

    We can also create words of different types:

    >>> word2 = Word("http://www.github.com", Word.TYPE_URL)
    >>> word2
    Word('http://www.github.com', word_type=2)

    If we don't specify the word type, the code will try to determine
    its type on its own:

    >>> word3 = Word("http://www.github.com")
    >>> print(word3)
    http://www.github.com
    >>> word4 = Word("@enfors")
    >>> word4
    Word('@enfors', word_type=3)

    We can also do comparisons:

    >>> word5 = Word("hello")
    >>> word6 = Word("there")
    >>> word7 = Word("hello")
    >>> word5 == word6
    False
    >>> word5 == word7
    True
    """

    TYPE_WORD = 1
    TYPE_URL = 2
    TYPE_USERNAME = 3
    TYPE_TAG = 4

    def __init__(self, word_text, word_type=None, keep_case=None):

        if word_type is None:
            if "://" in word_text:
                word_type = Word.TYPE_URL
            elif word_text[0] == "@":
                word_type = Word.TYPE_USERNAME
                if keep_case is None:
                    keep_case = True
            elif word_text[0] == "#":
                word_type = Word.TYPE_TAG
            else:
                word_type = Word.TYPE_WORD

        if keep_case is not True:
            word_text = word_text.lower()
                
        self.word_text = word_text
        self.word_type = word_type

    def __repr__(self):
        return "Word('%s', word_type=%d)" % (self.word_text, self.word_type)

    def __str__(self):
        return self.word_text

    def __len__(self):
        return len(self.word_text)

    def __eq__(self, other_word):
        if self.word_text == other_word.word_text:
            return True
        else:
            return False


class Sentence(list):
    # """Store a sentence in the form of a list of words.

    # >>> sentence = Sentence(["some", "words"])
    # >>> " ".join(sentence)
    # 'some words'
    # """

    pass


def normalize(text):
    """Return a normalized copy of text.
    """

    text = normalize_whitespace(text)
    text = unify_sentence_dividers(text)
    text = remove_junk_chars(text)

    return text


def unify_sentence_dividers(text):
    """Return copy of text with ? and ! replaced with .
    """

    for ch in ["!", "?"]:
        text = text.replace(ch, ".")

    return text


def remove_junk_chars(text):
    """Return copy of text without unneeded chars.
    """

    for ch in [",", ":", ";"]:
        text = text.replace(ch, "")

    return text


def split_sentences(text):
    """Attempt to split a text into sentences.
    """

    text = normalize_whitespace(text)
    text.replace("!", ".")
    text.replace("?", ".")
    sentences = [sentence.strip() for sentence in text.split(". ")]

    sentences[-1] = sentences[-1].rstrip(".")

    return sentences


def split_sentence(text):
    """Given a normalized sentence, return a list of Words.
    """

    words = []
    for part in text.split(" "):
        words.append(Word(part))

    return words


def normalize_and_split_sentences(text):
    """Return normalized sentences.

    >>> normalize_and_split_sentences("Foo bar. Another small sentence.")
    ['Foo bar', 'Another small sentence']
    >>> normalize_and_split_sentences(" Foo bar. Another  small sentence.")
    ['Foo bar', 'Another small sentence']
    >>> normalize_and_split_sentences("Foo bar . Another  small sentence.")
    ['Foo bar', 'Another small sentence']
    """

    text = normalize(text)
    sentences = split_sentences(text)

    return sentences


def normalize_whitespace(text):
    """Return a copy of text with one space between all words, with all
    newlines and tab characters removed.

    >>> print(normalize_whitespace("some text"))
    some text
    >>> print(normalize_whitespace(" some text "))
    some text
    >>> print(normalize_whitespace(" some   text"))
    some text
    >>> print(normalize_whitespace('\t\tsome text'))
    some text
    >>> print(normalize_whitespace("  some       text "))
    some text
    """

    new_text = text.replace("\n", " ")
    new_text = new_text.replace("\r", "")
    new_text = new_text.replace("\t", " ")

    words = [word.strip() for word in new_text.split(" ") if len(word) > 0]
    new_text = " ".join(words)
    return new_text

class NGram(object):
    """The ngram class stores an n-gram.

    Given a list of words, an n-gram is created. If a list of two words
    is provided, a bi-gram is created. If three words are provided, a
    3-gram is created, and so on.

    >>> word1 = Word("some")
    >>> word2 = Word("words")
    >>> bi_gram = NGram([word1, word2])
    >>> bi_gram
    NGram([Word('some', word_type=1), Word('words', word_type=1)])
    >>> print(bi_gram)
    some words
    >>> len(bi_gram)
    2

    We can also do comparisons:

    >>> word1 = Word("one")
    >>> word2 = Word("two")
    >>> word3 = Word("one")
    >>> ngram1 = NGram([word1, word2])
    >>> ngram2 = NGram([word3, word2])
    >>> ngram1 == ngram2
    True
    >>> ngram3 = NGram([word1, word2, word3])
    >>> ngram1 == ngram3
    False
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

    def __eq__(self, other_ngram):
        if len(self) != len(other_ngram):
            return False

        for i in range(0, len(self.words)):
            if self.words[i] != other_ngram.words[i]:
                return False

        return True


def make_ngrams(words, n):
    """Return n-grams from a list of Words.
    """

    num_words = len(words)
    index = 0
    n_grams = []

    while index + n <= num_words:
        n_gram = NGram(words[index:index + n])
        n_grams.append(n_gram)
        index = index + 1

    return n_grams


def demo():
    """Demonstrate the functionality in action.
    """

    import textwrap

    text = """
This is some text, split into several sentences over a number
of lines. Let's see what we can do with it. It's still a bit
short though, so I should probably make it longer by adding
more and more nonsense that noone wants to read. But that's\r\n
okay, since it's not meant to be read by humans.\r\n

The most merciful thing in the world, I think, is the human
mind's inability to correlate all its contents.

That is not dead which can eternal lie,
and with strange aeons, even death may die.
"""
    sentences = normalize_and_split_sentences(text)
    sentence = sentences[5]

    for sentence in sentences:
        print("%s." % "\n".join(textwrap.wrap("  " + sentence)))

    print("sentence:", sentence)

    print("\nbi-grams:")

    n_grams = make_ngrams(split_sentence(sentence), 2)

    for n_gram in n_grams:
        print(str(n_gram))

    print("\n3-grams:")

    ngrams = make_ngrams(split_sentence(sentence), 3)

    for ngram in ngrams:
        print(ngram)

    # print("\n4-grams:")

    # ngrams = make_ngrams(split_sentence(sentence), 4)

    # for ngram in ngrams:
    #     print(ngram)


if __name__ == "__main__":
#    demo()
    doctest.testmod()

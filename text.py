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


def set_sentence_value(sentence, value, min_n, max_n, ngram_matrix):
    """Give a value to a sentence, and all its ngrams.
    """

    for n in range(min_n, max_n + 1):
        ngrams = make_ngrams(split_sentence(sentence), n)

        for ngram in ngrams:
            dict_key = str(ngram)

            try:
                ngram_values = ngram_matrix[n][dict_key]
            except KeyError:
                ngram_values = []

            ngram_values.append(value)
            ngram_matrix[n][dict_key] = ngram_values


def get_sentence_value(sentence, min_n, max_n, ngram_matrix):
    """Get the value for a sentence.
    """

    all_values = []

    for n in range(min_n, max_n + 1):
        ngrams = make_ngrams(split_sentence(sentence), n)

        for ngram in ngrams:
            dict_key = str(ngram)
            value_sum = 0

            try:
                values = ngram_matrix[n][dict_key]
                for value in values:
                    value_sum = value_sum + value

                avg = value_sum / len(values)

                # Multiply the average with n, to weigh it.
                # 3-gram matches are three times more significant than
                # unigram matches.
                all_values.append(avg * n)
            except KeyError:
                pass  # This ngram didn't exist

    try:
        avg = sum(all_values) / len(all_values)
    except ZeroDivisionError:
        avg = 0

    print("Value for '%s': %d" % (sentence, avg))

    return avg


def demo():
    """Demonstrate the functionality in action.
    """

    # text = """
    # This is some text, split into several sentences over a number
    # of lines. Let's see what we can do with it. It's still a bit
    # short though, so I should probably make it longer by adding
    # more and more nonsense that noone wants to read. But that's\r\n
    # okay, since it's not meant to be read by humans.\r\n

    # The most merciful thing in the world, I think, is the human
    # mind's inability to correlate all its contents.

    # That is not dead which can eternal lie,
    # and with strange aeons, even death may die.
    # """
    # sentences = normalize_and_split_sentences(text)
    # sentence = sentences[5]
    # sentence = "That is not dead which can eternal lie"

    ngram_matrix = [{},
                    {},
                    {},
                    {}]

    min_n = 1
    max_n = 3

    print("min_n: %d, max_n: %d" % (min_n, max_n))

    train_data = [
        ["helt klart århundradets bästa film", 95],
        ["en film i absolut världsklass", 90],
        ["det här är årets bästa film alla kategorier", 85],
        ["så jävla bra", 83],
        ["jag är övertygad om att om 20 år kommer alla säga att detta "
         "är en klassiker", 80],
        ["en jättebra film helt enkelt", 78],
        ["en mycket bra film", 75],
        ["den var riktigt bra måste jag säga", 75],
        ["jättebra film skulle vilja se fler av samma regisör", 75],
        ["en riktigt bra film", 70],
        ["perfekt för en mysig hemmakväll", 65],
        ["den var förvånande nog ganska bra ändå", 60],
        ["den här filmen var helt okej tycker jag", 50],
        ["jag skulle gärna se fler såna här filmer", 40],
        ["jag tyckte väl att den var ganska bra", 30],
        ["den duger en regning kväll", 25],
        ["godkänd men inte mer än så skulle jag säga", 20],
        ["knappt godkänd men har sina poänger", 15],
        ["den kunde ha varit värre", 10],
        ["inte den bästa jag sett men inte det sämsta heller", 0],
        ["vad ska man säga det var inget man vill se igen direkt", -15],
        ["en småtråkig film måste jag säga", -10],
        ["den var tråkig vill inte se den igen", -20],
        ["mycket tråkig film tycker jag", -30],
        ["den var jättetråkig", -30],
        ["den var ganska dålig faktiskt", -30],
        ["det här var inget mästerverk direkt", -35],
        ["en riktigt dålig film", -50],
        ["rent skräp finns inget annat att säga", -65],
        ["hur sopig som helst", -70],
        ["den här filmen suger helt enkelt", -75],
        ["fattar inte hur en film kan vara så dålig", -75],
        ["filmen suger stenhårt", -80],
        ["det var 90 minuter av mitt liv jag aldrig kommer att få "
         "tillbaka", -80],
        ["detta var rent skräp finns inget annat att säga", -80],
        ["en riktig jävla skitfilm", -85],
        ["den var riktigt jävla sämst", -87],
        ["århundradets sämsta film alla kategorier", -90],
        ["det är den sämsta film jag någonsin sett", -90],
        ["aldrig har mänligheten utsatts för värre smörja en detta", -95],
        ]

    test_data = [
        "århundradets bästa film enligt min mening",
        "det här är min nya favoritfilm",
        "jag tyckte den var jättebra",
        "en ganska bra film",
        "vill gärna se den igen någon gång",
        "den var väl okej",
        "den var skitdålig",
        "sämsta jag har sett på länge",
        "århundradets skitfilm alla kategorier",
        "skräp helt enkelt",
        ]

    for d in train_data:
        set_sentence_value(d[0], d[1], min_n, max_n, ngram_matrix)

    for d in test_data:
        get_sentence_value(d, 1, 3, ngram_matrix)


if __name__ == "__main__":
    demo()
    doctest.testmod()

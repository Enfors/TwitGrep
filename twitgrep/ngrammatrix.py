#!/usr/bin/env python

"""Keep track of NGrams in a matrix.
"""

class NGramMatrix(object):
    """A list of dicts, where each dict will hold NGrams.
    """

    def __init__(self, min_n, max_n):
        self.min_n = min_n
        self.max_n = max_n
        self.matrix = []

        for n in range(0, max_n + 1):
            self.matrix.append({})

    def set_sentence_value(self, sentence, data):
        """Give a value to a sentence, and all its ngrams.
        """

        for n in range(self.min_n, self.max_n + 1):
            ngrams = make_ngrams(split_sentence(sentence), n)

            for ngram in ngrams:
                dict_key = str(ngram)

                try:
                    ngram_data = self.matrix[n][dict_key]
                except KeyError:
                    ngram_data = []

                ngram_data = self.add_data(ngram_data, data)
                self.matrix[n][dict_key] = ngram_data

    def add_data(self, ngram_data, data):
        """Add data to ngram_data. This function must be overridden, and must
        return ngram_data.
        """
        
        print("ERROR: NGramMatrix.add_data() not overridden.")

    def get_sentence_value(self, sentence):
        """Get the value for a sentence.
        """

        all_values = []

        for n in range(self.min_n, self.max_n + 1):
            ngrams = make_ngrams(split_sentence(sentence), n)

            for ngram in ngrams:
                dict_key = str(ngram)
                value_sum = 0

                try:
                    values = self.matrix[n][dict_key]
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

        return avg

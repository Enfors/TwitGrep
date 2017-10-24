#!/usr/bin/python3

"""Run sentiment analysis on Twitter.
"""

import twitgrep
import text


class TwitSent(object):
    """A class for running sentiment analysis on Twitter.
    """

    def __init__(self):
        pass

    def run(self):
        X = self.load_data("tweets.csv")
        model = self.make_model(X)

        self.stream_tweets(X, model)

    def load_data(self, path):
        """Load and previously downloaded sentences from secondary storage.
        """
        pass

    def make_model(self, X):
        """Build and return a sentiment analysis model based on X.
        """
        pass

    def stream_tweets(self, X, model):
        """Stream tweets and analyze them in real time.
        """

        search_term = "#svpol"

        try:
            for status in twitgrep.TwitGrep([search_term]):
                if status.text.startswith("RT @"):
                    continue
                if "…" in status.text:
                    continue
                print(self.format_tweet_for_csv(status, search_term) +
                      "--------")
        except KeyboardInterrupt:
            print()
            raise SystemExit

    def format_tweet_for_csv(self, status, search_term):
        """Return a string formatted for writing to a CSV file.
        """

        output = ""

        sentences = text.normalize_and_split_sentences(status.text)

        for sentence in sentences:
            output += "%s,%s,%s,,\n" % (search_term,
                                        status.user.screen_name,
                                        sentence)

        return output


if __name__ == "__main__":
    TwitSent().run()

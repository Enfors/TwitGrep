#!/usr/bin/python3

"""Run sentiment analysis on Twitter.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base

from twitgrep import text
from twitgrep import grep

Base = declarative_base()


class TweetPart(Base):
    """A class for storing tweets.
    """

    __tablename__ = "tweet_part"
    ident = Column(Integer, primary_key=True)
    search_term = Column(String)
    user = Column(String)
    pre_text = Column(String)
    post_text = Column(String)
    time = Column(DateTime, default=func.now())
    sentiment = Column(Integer)
    target = Column(Integer)


class TwitSent(object):
    """A class for running sentiment analysis on Twitter.
    """

    def __init__(self):
        self.engine = create_engine("sqlite:///tweets.sqlite")
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)

        Base.metadata.create_all(self.engine)

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

        s = self.session()
        search_term = "#svpol"

        try:
            for status in grep.TwitGrep([search_term]):
                if status.text.startswith("RT @"):
                    continue
                if "…" in status.text:
                    continue

                sentences = text.normalize_and_split_sentences(status.text)
                print("\nTweet from %s:" % status.user.screen_name)
                for sentence in sentences:
                    self.handle_sentence(sentence, search_term, status, s)

        except KeyboardInterrupt:
            print()
            raise SystemExit

    def handle_sentence(self, sentence, search_term, status, s):
        """Handle sentence (part of a tweet).
        """

        print(" ", sentence)
        parts = sentence.split(" ")
        post_sentence = ""
        for part in parts:
            word = text.Word(part)
            if word.word_type != word.TYPE_URL:
                post_sentence += str(word) + " "

        post_sentence = text.remove_junk_chars(post_sentence.strip().lower())

        if len(post_sentence) < 1:
            return False

        print("  -", post_sentence)
        part = TweetPart(search_term=search_term,
                         user=status.user.screen_name,
                         pre_text=sentence,
                         post_text=post_sentence,
                         sentiment=None,
                         target=None)
        s.add(part)
        s.commit()

    def set_target(self, tweet, target):
        """Set a user-defined target sentiment on a tweet part.
        """

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

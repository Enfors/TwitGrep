#!/usr/bin/python3

"""Run sentiment analysis on Twitter.
"""

import sqlalchemy
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
        self.engine = create_engine("sqlite:////home/enfors/devel/" +
                                    "python/TwitGrep/twitgrep/tweets.sqlite")
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)

        Base.metadata.create_all(self.engine)

        self.search_term="#svpol"

    def run(self):
        model = self.make_model(search_term=self.search_term, min_n=1, max_n=3)

        self.stream_tweets(self.search_term, model)

    def load_labeled_data(self, search_term):
        """Load and previously downloaded sentences from secondary storage.
        """
        s = self.session()
        # return s.query(TweetPart).from_statement(sqlalchemy.text("select * from "
        #                                                          "tweet_part where "
        #                                                          "label is not "
        #                                                          "null").all())
        data = s.query(TweetPart).filter(TweetPart.target != None).all()
        print("TwitSent(): Loaded %d rows of data." % len(data))
        return data

    def make_model(self, search_term, min_n, max_n):
        """Build and return a sentiment analysis model based on X.
        """
        model = text.NGramMatrix(min_n, max_n)

        tweet_parts = self.load_labeled_data(search_term)

        for tweet_part in tweet_parts:
            model.set_sentence_value(tweet_part.post_text, tweet_part.target)

        return model

    def stream_tweets(self, search_term, model):
        """Stream tweets and analyze them in real time.
        """

        s = self.session()

        try:
            for status in grep.TwitGrep([search_term]):
                if status.text.startswith("RT @"):
                    continue
                if "…" in status.text:
                    continue

                sentences = text.normalize_and_split_sentences(status.text)
                print("\nTweet from %s:" % status.user.screen_name)
                for sentence in sentences:
                    self.handle_sentence(sentence, search_term, status, s, model)

        except KeyboardInterrupt:
            print()
            raise SystemExit

    def handle_sentence(self, sentence, search_term, status, s, model):
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

        print("  - My estimation: %.2f" % model.get_sentence_value(post_sentence))
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

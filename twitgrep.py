#!/usr/bin/env python2.7
"Script to search Twitter in real time."

from __future__ import print_function

import os
import Queue
import threading

import tweepy

class TwitterThread(threading.Thread):
    def __init__(self, msg_queue, keywords):
        super(TwitterThread, self).__init__()
        self.msg_queue = msg_queue
        self.keywords = keywords
        self.listener = None
        self.stream = None

        # Set up Twitter authorizations.
        self.access_token = self.read_private("access_token")
        self.access_token_secret = self.read_private("access_token_secret")
        self.consumer_key = self.read_private("consumer_key")
        self.consumer_secret = self.read_private("consumer_secret")
        self.auth = tweepy.OAuthHandler(self.consumer_key,
                                        self.consumer_secret)
        self.auth.set_access_token(self.access_token,
                                   self.access_token_secret)


    def run(self):
        super(TwitterThread, self).__init__()
        self.listener = Listener(self.msg_queue)

        # Start listening for incoming tweets.
        self.stream = tweepy.Stream(self.auth, self.listener)

        # Instead of listening for tweets from users I follow, search
        # all of Twitter in real time for these keywords.
        self.stream.filter(track=self.keywords)

    @staticmethod
    def read_private(file_name):
        """Return the contents of a file in the private/ directory.
        The purpose of this is to not have to have secrets hardcoded
        in this file."""

        with open(os.path.join("private", file_name), "r") as file_handle:
            return file_handle.read().strip()



class TwitGrep(object):
    "TwitGrep class. It's an iterator."

    def __init__(self, keywords):
        self.twitter_thread = None
        self.keywords = keywords
        self.msg_queue = Queue.Queue()


    def __iter__(self):
        "This is called when iteration starts."
        # Start a separate thread for listening to stuff from Twitter.
        # When it detects something, it will send a message (on msg_queue)
        # to the main thread (this one).
        self.twitter_thread = TwitterThread(self.msg_queue, self.keywords)
        self.twitter_thread.start()

        return self

    def next(self):
        "This is called on each iteration."
        # Wait for the next message from the Twitter thread.
        # No telling how long this will take - perhaps everybody on
        # Twitter is shutting up today (HA!).
        stat = self.msg_queue.get()
        return stat


class Listener(tweepy.streaming.StreamListener):

    def __init__(self, msg_queue):
        super(Listener, self).__init__()

        self.msg_queue = msg_queue

    def on_status(self, status):
        """Tweepy (the Python Twitter wrapper used) calls this function
        whenever there's a new incoming status."""
        self.msg_queue.put(status)
        return True

    def on_error(self, status):
        "Called by Tweepy when it gets an error message from Twitter."
        print("ERROR: %s" % str(status))


if __name__ == "__main__":

    # Example of how to use this code to search for "python" and "#svpol":

    for status in TwitGrep(["python", "#svpol"]):
        print("----------------------------\nTweet from user '%s':\n%s" % \
              (status.user.screen_name, status.text))

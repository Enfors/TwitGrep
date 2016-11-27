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
        self.stream = tweepy.Stream(self.auth, self.listener)
        self.stream.filter(track=self.keywords)

    @classmethod
    def read_private(cls, file_name):
        "Return the contents of a file in the private/ directory."

        with open(os.path.join("private", file_name), "r") as file_handle:
            return file_handle.read().strip()



class TwitGrep(object):
    "TwitGrep class."

    def __init__(self, keywords):
        self.twitter_thread = None
        self.keywords = keywords
        self.msg_queue = Queue.Queue()


    def __iter__(self):
        self.twitter_thread = TwitterThread(self.msg_queue, self.keywords)
        self.twitter_thread.start()

        return self

    def next(self):
        "Needed for the iterator framework."
        stat = self.msg_queue.get()
        return stat


class Listener(tweepy.streaming.StreamListener):

    def __init__(self, msg_queue):
        super(Listener, self).__init__()

        self.msg_queue = msg_queue

    def on_status(self, status):
        self.msg_queue.put(status)
        return True

    def on_error(self, status):
        print("ERROR: %s" % str(status))


if __name__ == "__main__":
    for status in TwitGrep(["python", "#svpol"]):
        print("----------------------------\nTweet from user '%s':\n%s" % \
              (status.user.screen_name, status.text))
        #print("User: %s" % status.user)

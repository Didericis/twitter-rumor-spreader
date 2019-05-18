from twitterscraper.query import query_tweets_from_user
import json
import os


"""
This class downloads all of the tweets for a particular user and classifies
which of those tweets have been retweeted. NOTE: not all of the information
downloaded is necessarily used when calculating the likelihood of a retweet,
but has been downloaded in anticipation of future changes.
"""
class Node():
    DATA_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data'
    )

    def __init__(self, username):
        self.username = username

    @property
    def filename(self):
        return '{}/{}.json'.format(self.DATA_DIR, self.username)

    def download(self):
        print('\n===={}===='.format(self.username))
        self.is_complete = False
        self.retweeted = {}
        self.tweeted = {}
        self.num_retweets_by_originator = {}
        self.users_retweeted = []

        # if a user has already been downloaded, we don't want to do it again,
        # so we load the user from the cache instead
        print(self.filename)
        if os.path.isfile(self.filename):
            print('Loading from cache...')
            self.load()

        if self.is_complete:
            return self
        else:
            self._download_tweeted_and_retweeted()
            self.is_complete = True
            self.save()
            return self

    def load(self):
        with open(self.filename, 'r') as file:
            obj = json.load(file)
            self.is_complete = True
            self.username = obj['username']
            self.retweeted = obj['retweeted']
            self.tweeted = obj['tweeted']
            self.num_retweets_by_originator = obj['num_retweets_by_originator']
            self.users_retweeted = obj['users_retweeted']

    def serialize(self):
        return {
            'is_complete': self.is_complete,
            'username': self.username,
            'retweeted': self.retweeted,
            'tweeted': self.tweeted,
            'num_retweets_by_originator': self.num_retweets_by_originator,
            'users_retweeted': self.users_retweeted,
        }

    def _serialize_tweet(self, tweet):
        return {
            'id': tweet.id,
            'text': tweet.text,
            'username': tweet.user,
            'num_likes': tweet.likes,
            'num_retweets': tweet.retweets,
            'num_replies': tweet.replies,
        }

    def save(self):
        if not os.path.isdir(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)

        print('Saving {}...'.format(self))
        with open(self.filename, 'w') as fp:
            json.dump(self.serialize(), fp, indent=4)

    def _download_tweeted_and_retweeted(self):
        print('Downloading tweeted and retweeted...')
        for tweet in query_tweets_from_user(self.username):
            if tweet.user != self.username:
                occurences = self.num_retweets_by_originator.get(tweet.user, 0)
                self.num_retweets_by_originator[tweet.user] = occurences + 1
                self.retweeted[tweet.id] = self._serialize_tweet(tweet)
            else:
                self.tweeted[tweet.id] = self._serialize_tweet(tweet)
        self.users_retweeted = list(map(
            lambda item: item[0],
            sorted(
                self.num_retweets_by_originator.items(),
                key=lambda item: item[1], reverse=True
            )
        ))

    def __str__(self):
        return self.username

from nltk.tokenize import TweetTokenizer
import json
import os

from twitter_network import TwitterNetwork
from node import Node


"""
This class is responsible for counting the positive and negative occurences
of certain tokens per user. Once run, it saves the probabilities it counts to
disk.
"""
class RelationshipTrainer():
    TRAINING_RESULTS_FILENAME = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'by_username.json'
    )

    tknzr = TweetTokenizer(preserve_case=False)

    def __init__(self):
        with open(TwitterNetwork.FILE_NAME, 'r') as file:
            self.network = json.load(file)
            file.close()
        self.by_username = {}

    def train(self):
        print('Training...')
        for username in self.network.keys():
            self.count_tweets(username)

    def _load_user_data(self, username):
        with open(os.path.join(Node.DATA_DIR, '{}.json'.format(username)), 'r') as file:
            return json.load(file)

    def _get_retweeted_tokens(self, username):
        user = self._load_user_data(username)
        return self.tknzr.tokenize(" ".join(map(
            lambda d: d['text'], user['retweeted'].values()
        )))

    def _get_not_retweeted_tokens(self, username):
        user = self._load_user_data(username)

        not_retweeted_tokens = []
        for network in self.network[username]:
            other_user = self._load_user_data(username)
            for id, tweet in other_user['tweeted'].items():
                if id not in user['retweeted']:
                    not_retweeted_tokens += self.tknzr.tokenize(tweet['text'])
            for id, tweet in other_user['retweeted'].items():
                if id not in user['retweeted']:
                    not_retweeted_tokens += self.tknzr.tokenize(tweet['text'])
        return not_retweeted_tokens

    def _count_tokens(self, username, tokens, is_positive=False):
        user_data = self.by_username.get(username, {
            'total_negative': 0,
            'total_positive': 0,
            'total': 0,
            'words': {}
        })
        for token in tokens:
            result = user_data['words'].get(token, {
                'positive': 0,
                'negative': 0,
                'total': 0
            })
            if is_positive:
                result['positive'] += 1
                user_data['total_positive'] += 1
            else:
                result['negative'] += 1
                user_data['total_negative'] += 1
            result['total'] += 1
            user_data['total'] += 1
            user_data['words'][token] = result
        self.by_username[username] = user_data

    def count_tweets(self, username):
        print('Counting tweets for {}...'.format(username))
        positive_tokens = self._get_retweeted_tokens(username)
        negative_tokens = self._get_not_retweeted_tokens(username)
        self._count_tokens(username, positive_tokens, is_positive=True)
        self._count_tokens(username, negative_tokens, is_positive=False)
        print({
            'total_negative': self.by_username[username]['total_negative'],
            'total_positive': self.by_username[username]['total_positive'],
            'total': self.by_username[username]['total']
        })
        self._save()

    def _save(self):
        print('Saving...')
        with open(RelationshipTrainer.TRAINING_RESULTS_FILENAME, "w") as dump_file:
            json.dump(self.by_username, dump_file, indent=2)

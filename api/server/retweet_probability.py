import json
import os
import math
import random

from relationship_trainer import RelationshipTrainer

# The proabilities are loaded into memory on start
filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), RelationshipTrainer.TRAINING_RESULTS_FILENAME)
all_probabilities = {}
with open(filepath, 'r') as file:
    all_probabilities = json.load(file)
    file.close()


# This function returns the probability a given user will retweet a given tweet using
# the formula for Naive Bayes Classifiers
def retweet_probability(username, tweet):
    probabilities = all_probabilities.get(username, {
        # we assume our totals are 1 so that we never end up dividing by zero
        'total_positive': 1,
        'total_negative': 1,
        'total': 1,
        'words': {}
    })
    tokens = RelationshipTrainer.tknzr.tokenize(tweet)

    # we assume our totals are 1 so that we never end up dividing by 0
    total_positive_token_occurences = float(probabilities['total_positive'] or 1)
    total_negative_token_occurences = float(probabilities['total_negative'] or 1)
    total_token_occurences = float(probabilities['total'] or 1)

    probability_class_is_positive = float(total_positive_token_occurences/total_token_occurences)
    probability_class_is_negative = float(total_negative_token_occurences/total_token_occurences)

    positive_prob = probability_class_is_positive
    negative_prob = probability_class_is_negative

    token_specific_calculations = {}
    for token in tokens:
        token_counts = probabilities['words'].get(token, {'positive': 0, 'negative': 0, 'total': 0})
        this_token_total_occurences = float(token_counts.get('total'))

        # if we don't have any positive token occurences, we use the default probability a class is positive so that our
        # probabilities aren't sent to 0
        this_token_positive_occurences = float(token_counts.get('positive') or probability_class_is_positive)
        probability_this_token_positive = float(this_token_positive_occurences / total_positive_token_occurences)
        positive_prob = float(positive_prob * probability_this_token_positive)

        # if we don't have any negative token occurences, we use the default probability a class is negative so that our
        # probabilities aren't sent to 0
        this_token_negative_occurences = float(token_counts.get('negative') or probability_class_is_negative)
        probability_this_token_negative = float(this_token_negative_occurences / total_negative_token_occurences)
        negative_prob = float(negative_prob * probability_this_token_negative)

        token_specific_calculations[token] = {
            'probability_is_positive': probability_this_token_positive,
            'probability_is_negative': probability_this_token_negative,
            'total_occurences': this_token_total_occurences
        }

    retweet_probability_average = float(probability_class_is_positive / (probability_class_is_positive + probability_class_is_negative))
    retweet_probability = float(positive_prob / ((negative_prob + positive_prob) or 1))

    return {
        # this term indicates the output for the naive bayesian classification as a positive class
        'positive': positive_prob,
        # this term indicates the output for the naive bayesian classification as a negative class
        'negative': negative_prob,
        # this term indicates the average probability of a tweet being retweeted, regardless of content
        'retweet_probability_average': retweet_probability_average,
        # this term indicates the probability of this specific tweet being retweeted
        'retweet_probability': retweet_probability,
        # this term indicates how much more likely a tweet is to be retweeted than the average tweet
        'multiplier': float(retweet_probability / retweet_probability_average),
        # this term centers the multiplier around 0 so that a multiplier that does nothing (ie, is 1) is 0,
        # those that increase the probability are positive, and those that decrease the probability are negative
        'factor_scale': float((retweet_probability / retweet_probability_average) - (retweet_probability_average / retweet_probability)),
        # this term returns the probabilities for the specific tokens present in the tweet
        'token_specific_calculationss': token_specific_calculations
    }

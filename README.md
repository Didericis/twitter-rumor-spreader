# twitter-rumor-spreader

This app simulates the spread of retweets through a small network of twitter users. It's trained on real users and real data using the [Naive Bayes Classification Algorithm](https://en.wikipedia.org/wiki/Naive_Bayes_classifier).

### Files of note

- The Naive Bayesian Classification algorithm is implemented in [retweet_probabilities.py](https://github.com/Didericis/twitter-rumor-spreader/blob/master/api/server/retweet_probability.py).
- The network is built via [twitter_network.py](https://github.com/Didericis/twitter-rumor-spreader/blob/master/api/server/twitter_network.py)
  - Actual tweets are downloaded via [node.py](https://github.com/Didericis/twitter-rumor-spreader/blob/master/api/server/node.py)
- The word counts used in the Naive Bayesian Classification algorithm are determined in [relationship_trainer.py](https://github.com/Didericis/twitter-rumor-spreader/blob/master/api/server/relationship_trainer.py)

### Running Locally

To run locally, you'll need git, docker, and docker-compose:

```sh
git clone https://github.com/Didericis/twitter-rumor-spreader.git
cd twitter-rumor-spreader
docker-compose up
```

Once running, the site will be available at `localhost:4000`.

### Live Version

A live version of the app can be found [here](http://ec2-3-86-97-50.compute-1.amazonaws.com/).

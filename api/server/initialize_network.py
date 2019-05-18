from node import Node
from twitter_network import TwitterNetwork
from relationship_trainer import RelationshipTrainer

# This script will create a twitter network for the given user

twitter_network = TwitterNetwork('fubuloubu').download()
for username, following in twitter_network.items():
    Node(username).download()
    for username in following:
        Node(username).download()

RelationshipTrainer().train()

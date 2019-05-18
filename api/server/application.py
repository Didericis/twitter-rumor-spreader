from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json

from retweet_probability import retweet_probability
from relationship_trainer import RelationshipTrainer
from twitter_network import TwitterNetwork
from node import Node

application = Flask(__name__)
CORS(application)

REPORT_FILENAME = 'latex/mat_488_final_project-eric_bauerfeld.pdf'

# This is the Flask server tha provides API endpoints to our react app


# this will return the probabilities associated with a particular user
@application.route("/probabilities/<username>")
def probabilities(username):
    filepath = RelationshipTrainer.TRAINING_RESULTS_FILENAME
    content = {}
    with open(filepath, 'r') as file:
        content = json.load(file)[username]
        file.close()
    return jsonify(content)


# this will determine what the probability is of a given tweet being retweeted by a particular user
@application.route("/retweet-prob", methods=['POST'])
def retweet_prob():
    input_json = request.get_json()
    result = retweet_probability(input_json['username'], input_json['tweet'])
    return jsonify(result)


# this will return our twitter network
@application.route("/network.json")
def network():
    filepath = TwitterNetwork.FILE_NAME
    content = {}
    with open(filepath, 'r') as file:
        raw_content = json.load(file)
        for key, value in raw_content.items():
            content[key] = list(filter(lambda k: k in raw_content.keys(), value))
        file.close()
    return jsonify(content)

# this will return all of the tweets associated with a particular user
# EX: /data/fubuloubu.json
@application.route("/data/<filename>")
def data(filename):
    filepath = os.path.join(Node.DATA_DIR, filename)
    content = {}
    with open(filepath, 'r') as file:
        content = json.load(file)
        file.close()
    return jsonify(content)

@application.route('/report.pdf')
def get_report():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        REPORT_FILENAME
    )

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)

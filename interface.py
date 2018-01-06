#!flask/bin/python
from flask import Flask, jsonify
import topicExtraction
import phraseExtraction

app = Flask(__name__)

@app.route('/api/topics/all/<string:business_id>', methods=['GET'])
def api_get_topics(business_id):
    topics = topicExtraction.get_topics(business_id)
    return jsonify(topics)

@app.route('/api/phrasees/all/<string:business_id>', methods=['GET'])
def api_get_phrases(business_id):
    ngrams = phraseExtraction.get_radical_ngrams(business_id)
    return jsonify(ngrams)

@app.route('/api/phrasees/noun_adj/<string:business_id>', methods=['GET'])
def api_get_pairs(business_id):
    pairs = phraseExtraction.get_radical_pairs(business_id)
    return jsonify(pairs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
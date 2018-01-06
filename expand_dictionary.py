import detectNLP
import wordnet

with open("topics.txt","r") as f:
    topics = f.readlines()

topic2words = dict()
for topic in topics:
    topic_name, topic_words = topic.split(":")
    topic_words = topic_words.split(",")


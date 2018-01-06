from langdetect import detect
import pickle
import json
from pymongo import MongoClient

def filter_language(reviews, collection, language = "en"):
    i = 0
    other_langs = 0
    while i < len(reviews):
        text = reviews[i]["text"]
        lang = detect(text)

        if lang != language:
            review_id = reviews[i]["review_id"]
            collection.delete_one({"_id": review_id})
            print(review_id)
            del reviews[i]
            other_langs += 1
        else:
            i += 1

    print("\nOther languages",other_langs)

if __name__ == "__main__":
    with open("database/config.json", "r") as f:
        config = json.load(f)

    client = MongoClient('mongodb://%s:%s@' % (config["username"], config["password"]) + config["url"] + '')
    db = client[config["db_name"]]
    collection = db['reviews']

    categories = ["Hotels", "Food"]
    for category in categories:
        with open("data/Las_Vegas-" + category + ".p", "rb") as f:
            all_reviews, business_id2business, user_id2user = pickle.load(f)
        filter_language(all_reviews, collection)
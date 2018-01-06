import json, pickle
from pymongo import MongoClient

def get_business_data_local(business_id):
    categories = ["Hotels","Food"]
    for category in categories:
        with open("data/Las_Vegas-" + category + ".p", "rb") as f:
            all_reviews, business_id2business, user_id2user = pickle.load(f)
        if business_id in business_id2business:
            break

    reviews = []
    business_name = business_id2business[business_id]["name"]
    for review in all_reviews:
        if review["business_id"] == business_id:
            reviews.append(review)

    return reviews, business_name

def get_business_data(business_id):
    with open("database/config.json", "r") as f:
        config = json.load(f)

    client = MongoClient('mongodb://%s:%s@' % (config["username"], config["password"]) + config["url"] + '')
    db = client[config["db_name"]]
    collection = db['reviews']
    reviews = collection.find({"business_id": business_id})
    collection = db['businesses']
    business = collection.find_one({'_id': business_id})
    business_name = business["name"]
    return reviews, business_name

def delete_review(review_id):
    with open("database/config.json", "r") as f:
        config = json.load(f)

    client = MongoClient('mongodb://%s:%s@' % (config["username"], config["password"]) + config["url"] + '')
    db = client[config["db_name"]]
    collection = db['reviews']
    collection.delete_one({"_id":review_id})
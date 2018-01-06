import pickle, json
import sys
from helper_functions import *
import detectNLP

verbs = ["like", "hate", "see", "watch", "eat", "enjoy", "walk"]

for verb in verbs:
    detectNLP.min_similar(verb)

sys.exit()

category = "Food"

all_reviews = []
user_id2user = dict()
business_id2business = dict()
with open("data/Las_Vegas-Food_businesses.json", 'r', encoding='utf-8') as f:
    for line in f:
        businesess = json.loads(line)
        for business in businesess:
            business_id2business[business["business_id"]] = business


with open("data/Las_Vegas-Food_reviews.json", 'r', encoding='utf-8') as f:
    for line in f:
        reviews = json.loads(line)
        for review in reviews:
            review["words"] = process_words(review["text"], "en",stem=True)
        all_reviews += reviews

with open("data/Las_Vegas-Food_users.json", 'r', encoding='utf-8') as f:
    for line in f:
        users = json.loads(line)
        for user in users:
            user_id2user[user["user_id"]] = user

with open("data/Las_Vegas-" + category + ".p", "wb+") as f:
    pickle.dump([all_reviews, business_id2business, user_id2user], f)

with open("data/Las_Vegas-Hotels.p", "rb") as f:
    reviews, business_id2business, user_id2user = pickle.load(f)

print("Hotels",len(reviews))

with open("data/Las_Vegas-Food.p", "rb") as f:
    reviews, business_id2business, user_id2user = pickle.load(f)

print("Food",len(reviews))


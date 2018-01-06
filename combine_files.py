import json, pickle
from helper_functions import *

with open("data/Las_Vegas-Hotels.p", "rb") as f:
    reviews, business_id2business, user_id2user = pickle.load(f)

print(len(business_id2business))

business_name2business_id = dict()
business_location2business_id = dict()
business_id2replacement = dict()

with open(r"dataset\tripAdvisor_review.json", 'r', encoding='utf-8') as f:
    for line in f:
        trip_advisor_reviews = json.loads(line)
        for review in trip_advisor_reviews:
            review["words"] = process_words(review["text"], "en",stem=True)
        reviews += trip_advisor_reviews


with open(r"dataset\business_tripAdvisor_good.txt", 'r', encoding='utf-8') as f:
    for line in f:
        businesses = json.loads(line)
        for business in businesses:
            business_id = business["business_id"]
            if(business_id in business_id2business):
                business_id2business[business_id] = business

for business_id in business_id2business:
    business = business_id2business[business_id]
    try:
        business["latitude"] = float(business["latitude"])
        business["longitude"] = float(business["longitude"])
        lat = round(business["latitude"],6)
        lon = round(business["longitude"],6)
        name = business["name"].lower().replace("[^0-9a-z]","")
        if (lat, lon) not in business_location2business_id:
            business_location2business_id[(lat, lon)] = business
        else:
            if name in business_name2business_id:
                business_id2replacement[business_id] = business_name2business_id[name]

        if name not in business_name2business_id:
            business_name2business_id[name] = business

    except Exception:
        print(business["name"])
        print(business["latitude"])
        print(business["longitude"])

for review in reviews:
    review["stars"] = float(review["stars"])
    if "words" not in review:
        review["words"] = process_words(review["text"], language="en" )
        if review["business_id"] in business_id2replacement:
            review["business_id"] = business_id2replacement[review["business_id"]]["business_id"]

businesses = []
for business_id in business_id2business:
    businesses.append(business_id2business[business_id])

with open("data/Las_Vegas-Hotels_reviews.json", "w") as f:
    json.dump(reviews, f)

with open("data/Las_Vegas-Hotels_businesses.json", "w") as f:
    json.dump(businesses, f)


with open("data/Las_Vegas-Hotels.p", "wb+") as f:
     pickle.dump([reviews, business_id2business, user_id2user],f)
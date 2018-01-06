import pickle
category = "Food"
with open("data/Las_Vegas-" + category + ".p", "rb") as f:
    all_reviews, business_id2business, user_id2user = pickle.load(f)

max_reviews = 0
average = [0,0]
for user_id in user_id2user:
    user = user_id2user[user_id]
    average[0] +=  user["review_count"]
    average[1] += 1
    if user["review_count"] > max_reviews:
        max_reviews = user["review_count"]

print(max_reviews)
print(float(average[0]) / average[1])
import pickle

categories = ["Food","Hotels"]
for category in categories:
    with open("data/Las_Vegas-" + category + ".p", "rb") as f:
        all_reviews, business_id2business, user_id2user = pickle.load(f)

    no_user_rating = 0.0
    no_user_total  = 0
    category_average_rating = 0.0
    business2rating_aux = dict()
    user2rating_aux = dict()
    for review in all_reviews:
        stars = float(review["stars"])
        category_average_rating += stars
        business_id = review["business_id"]
        if business_id not in business2rating_aux:
            business2rating_aux[business_id] = [0.0, 0]
        business2rating_aux[business_id][0] += stars
        business2rating_aux[business_id][1] += 1
        if "user_id" in review:
            if review["user_id"] not in user2rating_aux:
                user2rating_aux[review["user_id"]] = [0.0, 0]
            user2rating_aux[review["user_id"]][0] += stars
            user2rating_aux[review["user_id"]][1] += 1
        else:
            no_user_rating += stars
            no_user_total  += 1

    category_average_rating /= len(all_reviews)

    if no_user_total == 0:
        no_user_avg_rating = 0
    else:
        no_user_avg_rating = no_user_rating/no_user_total
    no_user_bias =  no_user_avg_rating - category_average_rating
    user2bias = dict()
    for user in user2rating_aux:
        user2bias[user] =  (user2rating_aux[user][0]/user2rating_aux[user][1]) - category_average_rating
        if user in user_id2user:
            user_id2user[user]["bias"] = user2bias[user]
        else:
            user_id2user[user] = {'user_id':user, 'name':user,"bias":user2bias[user],'review_count':user2rating_aux[user][1],'average_stars':user2rating_aux[user][0]/user2rating_aux[user][1]}

    business2bias = dict()
    for business in business2rating_aux:
        business2bias[business] = (business2rating_aux[business][0]/business2rating_aux[business][1]) - category_average_rating
        if business in business_id2business:
            business_id2business[business]["bias"] = business2bias[business]
        else:
            business_id2business[business] = {'business_id':business, 'name':business,"bias":business2bias[business],'review_count':business2rating_aux[business][1],'stars':business2rating_aux[business][0]/business2rating_aux[business][1] }

    user_id2user["trip_advisor_"+category] = {"user_id":"trip_advisor_"+category, 'name':"trip_advisor", 'review_count':no_user_total, "average_stars":no_user_avg_rating, "bias":no_user_bias}

    min_bias = 5.0
    max_bias = 0.0
    for review in all_reviews:
        stars = float(review["stars"])
        business_id = review["business_id"]
        business_bias = business2bias[business_id]
        if "user_id" in review:
            user_bias = user2bias[review["user_id"]]
        else:
            user_bias = no_user_bias

        review_bias = stars - category_average_rating - user_bias - business_bias
        review["bias"] = review_bias
        if review_bias > max_bias:
            max_bias = review_bias
        if review_bias < min_bias:
            min_bias = review_bias

    dif = max_bias - min_bias
    for review in all_reviews:
        review["normalized_bias"] = float(review["bias"]-min_bias)/dif

    with open("data/Las_Vegas-" + category + ".p", "wb+") as f:
        pickle.dump([all_reviews, business_id2business, user_id2user], f)

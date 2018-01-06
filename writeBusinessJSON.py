import pickle, json

categories = ["Hotels", "Food"]

restaurant_ids = ["RESDUcs7fIiihp38-d6_6g","DkYS3arLOhA8si5uUEmHOw","eoHdUeQDNgQ6WYEnP2aiRw","NvKNe9DnQavC9GstglcBJQ","xkVMIk_Vqh17f48ZQ_6b0w"]
hotel_ids      = ["SMPbvZLSMMb7KU76YNYMGg","5LNZ67Yw9RD6nf4_UhXOjw","AV6weBrZFFBfRGCbcRGO4g","El4FC8jcawUVgw_0EIcbaQ","Wxxvi3LZbHNIDwJ-ZimtnA"]

business2name    = dict()
business2reviews = dict()

category2filter_ids = {
    "Food":restaurant_ids,
    "Hotels":hotel_ids
}

for category in categories:
    with open("data/Las_Vegas-" + category + ".p", "rb") as f:
        all_reviews, business_id2business, user_id2user = pickle.load(f)

    filter_ids = category2filter_ids[category]

    for review in all_reviews:
        if review["business_id"] in filter_ids:
            if review["business_id"] not in business2reviews:
                business2reviews[review["business_id"]] = []
                business2name[review["business_id"]] = business_id2business[review["business_id"]]["name"]
            business2reviews[review["business_id"]].append(review)

    for business_id in filter_ids:
        name = business2name[business_id]
        reviews = business2reviews[business_id]
        with open("data/Las_Vegas-" + category + "-" + name + ".json", "w") as f:
            json.dump(reviews, f)
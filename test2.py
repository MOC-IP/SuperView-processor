n_features = 1000
n_components = 10
n_top_words = 20

print(get_sentence_sentiment_coreNLP("I have a big banana. You have a lovely bunch of coconuts."))

categories = ["Hotels"]

restaurant_ids = ["RESDUcs7fIiihp38-d6_6g","DkYS3arLOhA8si5uUEmHOw","eoHdUeQDNgQ6WYEnP2aiRw","NvKNe9DnQavC9GstglcBJQ","xkVMIk_Vqh17f48ZQ_6b0w"]
hotel_ids      = ["SMPbvZLSMMb7KU76YNYMGg","5LNZ67Yw9RD6nf4_UhXOjw","AV6weBrZFFBfRGCbcRGO4g","El4FC8jcawUVgw_0EIcbaQ","Wxxvi3LZbHNIDwJ-ZimtnA"]

business2name    = dict()
business2reviews = dict()



category2filter_ids = {
    "Foods":restaurant_ids,
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

    for index in range(len(hotel_ids)):
        print()
        if category == "Food":
            selected_business_id = restaurant_ids[index]
        elif category == "Hotels":
            selected_business_id = hotel_ids[index]

        selected_business_name = business2name[selected_business_id]
        reviews = business2reviews[selected_business_id]
        add_sentences_to_reviews_multithreaded(reviews)

        with open("data/Las_Vegas-" + category + ".p", "wb+") as f:
            pickle.dump([all_reviews, business_id2business, user_id2user], f)

        stars2texts = [[]] * 5
        for review in reviews:
            if "sentences" not in review:
                review["sentences"] = get_sentence_sentiment_coreNLP(review["text"], core_nlp=core_nlp)
            if len(review["sentences"]) == 0:
                continue
            star = float(review["stars"]) - 1
            average_sentiment = 0.0
            for sentence_sentiment in review["sentences"]:
                sentence = sentence_sentiment[0]
                sentiment= sentence_sentiment[1]
                average_sentiment += sentiment
            average_sentiment /= len(review["sentences"])
            average_sentiment += 1
            for sentence_sentiment in review["sentences"]:
                sentence = sentence_sentiment[0]
                sentiment= sentence_sentiment[1] + 1

                sentence_star = int(round((float(sentiment)/average_sentiment) * star))

                if sentence_star > 4:
                    sentence_star = 4

                stars2texts[sentence_star].append(sentence)

        print()
        print(selected_business_name)
        for j in range(4):
            if j == 0:
                data_samples = stars2texts[0]
                prefix = "Very negative"
            elif j == 1:
                data_samples = stars2texts[0] + stars2texts[1]
                prefix = "Negative"
            elif j == 2:
                data_samples = stars2texts[3] + stars2texts[4]
                prefix = "positive"
            elif j == 3:
                data_samples = stars2texts[4]
                prefix = "very positive"

            n_samples = len(data_samples)

            print("Extracting tf-idf features for NMF...")
            tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                               max_features=n_features,
                                               stop_words='english')
            t0 = time()
            tfidf = tfidf_vectorizer.fit_transform(data_samples)
            print("done in %0.3fs." % (time() - t0))

            # Use tf (raw term count) features for LDA.
            print("Extracting tf features for LDA...")
            tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                            max_features=n_features,
                                            stop_words='english')
            t0 = time()
            tf = tf_vectorizer.fit_transform(data_samples)
            print("done in %0.3fs." % (time() - t0))
            print()

            # Fit the NMF model
            print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
                  "n_samples=%d and n_features=%d..."
                  % (n_samples, n_features))
            t0 = time()
            nmf = NMF(n_components=n_components, random_state=1,
                      alpha=.1, l1_ratio=.5).fit(tfidf)
            print("done in %0.3fs." % (time() - t0))

            print("\n"+ prefix + " " + selected_business_name + " Topics in NMF model (Frobenius norm):")
            tfidf_feature_names = tfidf_vectorizer.get_feature_names()
            print_top_words(nmf, tfidf_feature_names, n_top_words)

            # Fit the NMF model
            print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
                  "tf-idf features, n_samples=%d and n_features=%d..."
                  % (n_samples, n_features))
            t0 = time()
            nmf = NMF(n_components=n_components, random_state=1,
                      beta_loss="kullback-leibler", solver='mu', max_iter=1000, alpha=.1,
                      l1_ratio=.5).fit(tfidf)
            print("done in %0.3fs." % (time() - t0))

            print("\n"+ prefix + " " + selected_business_name + " Topics in NMF model (generalized Kullback-Leibler divergence):")
            tfidf_feature_names = tfidf_vectorizer.get_feature_names()
            print_top_words(nmf, tfidf_feature_names, n_top_words)

            print("Fitting LDA models with tf features, "
                  "n_samples=%d and n_features=%d..."
                  % (n_samples, n_features))
            lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                            learning_method='online',
                                            learning_offset=50.,
                                            random_state=0)
            t0 = time()
            lda.fit(tf)
            print("done in %0.3fs." % (time() - t0))

            print("\n"+ prefix + " " + selected_business_name + " Topics in LDA model:")
            tf_feature_names = tf_vectorizer.get_feature_names()
            print_top_words(lda, tf_feature_names, n_top_words)

        get_radical_ngrams(reviews)

if False:
    categories = ["Food"]

    numberOfThreads = 4
    for category in categories:
        with open("data/Las_Vegas-"+category+".p", "rb") as f:
            reviews, business_id2business, user_id2user = pickle.load(f)

        step = len(reviews)//numberOfThreads
        split_reviews = [(reviews[step*i:step*(i+1)],i+9001) for i in range(numberOfThreads)]
        pool = ThreadPool(numberOfThreads)
        results = pool.map(add_sentences_to_reviews, split_reviews)

        with open("data/Las_Vegas-"+category+".p", "wb+") as f:
                pickle.dump([reviews, business_id2business, user_id2user], f)



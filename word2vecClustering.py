from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture, GMM
import numpy as np
import pickle
import detectNLP
import data_helpers
import gensim
from GloVe_tensorflow import *
from os.path import exists, join
import word_cloud

#can be "GloVe", "pretrainedWord2vec" or "category_trainedWord2vec"
wordvecType = "pretrainedWord2vec"

#can be "GaussianMixture", "KMeans", "DBSCAN" or "KMeansDBSCAN"
clusteringType = "GaussianMixture"

#set the number of clusters for KMeans
n_clusters = 10

X = []
words = []

category = "Hotels"
with open("data/Las_Vegas-" + category + ".p", "rb") as f:
    reviews, business_id2business, user_id2user = pickle.load(f)
del user_id2user
del business_id2business

word2count = dict()
corpus = []
for review in reviews:
    corpus.append(review["words"])
    for word in set(review["words"]):
        if word not in word2count:
            word2count[word] = 0
        word2count[word] += 1

del reviews

if wordvecType == "category_trainedWord2vec":
    model = gensim.models.word2vec.Word2Vec(corpus,size=300, iter=100)
    word2vec = model.wv
elif wordvecType == "GloVe":
    if exists("data/GloVe/" + category + ".bin"):
        with open("data/GloVe/" + category + ".bin", 'rb') as vector_f:
            word2vec = pickle.load(vector_f)
    else:
        model = GloVeModel(embedding_size=300, context_size=5)
        model.fit_to_corpus(corpus)
        print("Training")
        model.train(num_epochs=100)
        word2vec = dict()

        for text in corpus:
            for word in text:
                if word not in word2vec:
                    try:
                        word2vec[word] = model.embedding_for(word)
                    except Exception:
                        continue

        with open("data/GloVe/" + category + ".bin", 'wb+') as vector_f:
            pickle.dump(word2vec, vector_f)

elif wordvecType == "pretrainedWord2vec":
    word2vec = dict()
    for word in word2count:
        word2vec[word] = detectNLP.get_average_wordvec(word)
else:
    raise Exception("Invalid wordvecType")


cnt = 0
for word in word2count:
    try:
        wordVec = word2vec[word]
        if not np.isnan(wordVec).any():
            X.append(wordVec)
            words.append(word)
    except Exception:
        continue

if clusteringType=="KMeans":
    classifier = KMeans(n_clusters=n_clusters)
    predictions = classifier.fit_predict(X)
elif clusteringType == "GaussianMixture":
    classifier = GMM(n_components=1000, min_covar=0.0001)
    classifier.fit(X)
    predictions = classifier.predict(X)
elif clusteringType=="DBSCAN":
    classifier = DBSCAN(eps = 5, min_samples=100)
    predictions = classifier.fit_predict(X)
elif clusteringType=="KMeansDBSCAN":
    classifier = KMeans(n_clusters=n_clusters)
    predictions = classifier.fit_predict(X)
    subsets = [[]] * 10
    for i,prediction in enumerate(predictions):
        x = X[i]
        subsets[prediction].append(x)

    predictions = []
    current_cluster = 0
    for subset in subsets:
        classifier = DBSCAN(eps = 5
                            , min_samples=100)
        subpredictions = classifier.fit_predict(X)
        predictions.extend(map(lambda x: x + current_cluster, subpredictions))
        max_cluster = np.max(subpredictions)
        current_cluster += max_cluster
else:
    raise Exception("Invalid clusteringType")


word2cluster = dict()

cluster_texts = dict()
rows = [["Word","Cluster"]]
for i, word in enumerate(words):
    clusterNum = predictions[i]
    word2cluster[word] = clusterNum
    if clusterNum not in cluster_texts:
        cluster_texts[clusterNum] = []
    cluster_texts[clusterNum].extend([word]*word2count[word])

    rows.append([word, clusterNum])

for cluster in cluster_texts:
    text = " ".join(cluster_texts[cluster])
    output_filename = "images/"+category+"_"+wordvecType+"_"+clusteringType+"_cluster"+str(cluster)+".png"
    if category == "Hotels":
        mask_filename = "images/hotel3.jpg"
    elif category == "Food":
        mask_filename = "images/plate_gray.png"

    word_cloud.make_word_cloud(text,output_filename,mask_filename)

filename = "data/" + wordvecType + "-" + clusteringType + "-" + category+"_word2cluster.csv"
data_helpers.write_csv(filename, rows)
data_helpers.write_csv_to_xlsx(filename)

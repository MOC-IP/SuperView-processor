import spacy
import sys
nlp = spacy.load('en')
text = u'Goodtr food waz a beautiful surprise, its hard to find but the sushi here has been great. I found the tables very sturdy, it was a nice place. We listened to music that was nice. The view look good'
doc = nlp(text)
for token in doc:
    print(token.lemma_, token.dep_, token.head.text, token.head.pos_,
          [(child.text, child.pos_) for child in token.children])

def get_adj_noun_pairs(text):
    pairs = []
    doc = nlp(text)
    stopwords = ["-PRON-", "that"]
    for token in doc:
        if token.lemma_ == "be" or token.dep_ == "ROOT":
            adjs  = []
            nouns = []
            if token.lemma_ == "be" and token.dep_ == "relcl":
                if token.head.pos_ == "ADJ" and token.head.lemma_ not in stopwords:
                    adjs.append(token.head.lemma_)
                elif token.head.pos_ == "NOUN":
                    nouns.append(token.head.lemma_)


            for child in token.children:
                if child.pos_ == "ADJ" and child.lemma_ not in stopwords:
                    if len(nouns)>0:
                        while len(nouns)>0:
                            pairs.append([child.lemma_,nouns[0]])
                            del nouns[0]
                    else:
                        adjs.append(child.lemma_)
                if child.pos_ == "NOUN":
                    if len(adjs)>0:
                        while len(adjs)>0:
                            pairs.append([adjs[0],child.lemma_])
                            del adjs[0]
                    else:
                        nouns.append(child.lemma_)
        if token.dep_ == "amod" and token.lemma_ not in stopwords:
            pairs.append([token.lemma_, token.head.lemma_])
    return pairs

print(get_adj_noun_pairs(text))

sys.exit()

import pickle
import phraseExtraction
hotels = ["SMPbvZLSMMb7KU76YNYMGg", "5LNZ67Yw9RD6nf4_UhXOjw", "AV6weBrZFFBfRGCbcRGO4g", "El4FC8jcawUVgw_0EIcbaQ", "Wxxvi3LZbHNIDwJ-ZimtnA"]
food_businesses = ["RESDUcs7fIiihp38-d6_6g", "DkYS3arLOhA8si5uUEmHOw", "eoHdUeQDNgQ6WYEnP2aiRw", "NvKNe9DnQavC9GstglcBJQ", "xkVMIk_Vqh17f48ZQ_6b0w"]
category2businesses = {"Hotels":hotels, "Food":food_businesses}
for category in category2businesses:
    businesses = category2businesses[category]
    with open("data/Las_Vegas-" + category + ".p", "rb") as f:
        all_reviews, business_id2business, user_id2user = pickle.load(f)
    for business in businesses:
        print("\n\n\n"+business_id2business[business]["name"])
        phraseExtraction.get_radical_pairs(business)
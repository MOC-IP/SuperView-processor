import time
import unittest
from textblob import TextBlob
import numpy as np


def get_senitment_textblob(text):
    testimonial = TextBlob(text)
    return (testimonial.sentiment.polarity+1) / 2

def timing(f):
    def wrap(*args):
        time1 = time()
        ret = f(*args)
        time2 = time()
        print("Function " + str(f.__name__) + " took " + str(((time2-time1)*1000.0)) + " ms")
        if args:
            print("It had the following arguments",*args)
        else:
            print("It had no arguments")
        return ret
    return wrap

class TddFilterPhrases(unittest.TestCase):
    @timing
    def test_filter_phrases(self):
        word_ratings = [("best buffet life ", 5.0), ("eating day ", 5.0), ("easily best buffet ", 5.0),
                        ("horrible customer ", 1.0), ("horrible customer service ", 1.0), ("brunch includes ", 5.0),
                        ("ceasers palace ", 5.0), ("presentation dishes ", 5.0), ("buffet strip hands ", 5.0),
                        ("strip hands ", 5.0), ("place wo ", 5.0), ("place wo nt ", 5.0), ("vegas ve buffet ", 5.0),
                        ("noodles sushi ", 5.0), ("forget leave ", 5.0), ("fit food ", 5.0), ("yum yum yum ", 5.0),
                        ("completely worth ", 5.0), ("buffet hands best ", 5.0), ("food bacchanal buffet ", 5.0),
                        ("butter dispenser ", 5.0), ("vegas breakfast ", 5.0), ("worth single ", 5.0),
                        ("simply best ", 5.0), ("pricey worth penny ", 5.0), ("breakfast amazing ", 5.0),
                        ("told manager ", 1.0), ("worth single penny ", 5.0), ("single penny ", 5.0),
                        ("start buffet ", 5.0), ("brisket smoked ", 5.0), ("dollar dollar ", 5.0), ("cuts meats ", 5.0),
                        ("italian dessert ", 5.0), ("notch quality ", 5.0),
                        ("http wwwyelpcombizphotosresducsfiiihpdg selectywgfbzxkffoykutq ", 5.0),
                        ("wwwyelpcombizphotosresducsfiiihpdg selectywgfbzxkffoykutq ", 5.0), ("love thee ", 5.0),
                        ("buffet vegas hands ", 4.923076923076923), ("highly recommend place ", 4.909090909090909),
                        ("buffet ve food ", 4.909090909090909), ("food incredible ", 4.9), ("cheese bar ", 4.9),
                        ("wait vegas ", 4.9), ("selection incredible ", 4.9), ("meats asian ", 4.888888888888889),
                        ("time visit vegas ", 4.888888888888889), ("vegas hands ", 4.882352941176471),
                        ("hotel casino ", 4.875), ("juice horchata ", 4.875), ("totally worth money ", 4.875),
                        ("wait well worth ", 4.875), ("best dinner ", 4.875), ("pricey well worth ", 4.866666666666666),
                        ("wo nt regret ", 4.866666666666666), ("easily best ", 4.863636363636363),
                        ("covered strawberry ", 4.857142857142857), ("yum yum ", 4.857142857142857),
                        ("bacchanal disappoint ", 4.857142857142857), ("flavors mango ", 4.857142857142857),
                        ("worth ate ", 4.857142857142857), ("delicious service ", 4.857142857142857),
                        ("portions small ", 4.857142857142857), ("best brunch ", 4.857142857142857),
                        ("american buffet ", 4.857142857142857), ("worth cent ", 4.857142857142857),
                        ("place heaven ", 4.857142857142857), ("shrimp fish ", 4.857142857142857),
                        ("omg best ", 4.857142857142857), ("types gelato ", 4.857142857142857),
                        ("takes cake ", 4.857142857142857), ("soup sushi ", 4.857142857142857),
                        ("nt crack ", 4.857142857142857), ("omg place ", 4.857142857142857),
                        ("buffett vegas ", 4.857142857142857), ("omg food ", 4.857142857142857),
                        ("station lots ", 4.857142857142857), ("will definitely time ", 4.846153846153846),
                        ("ve best ", 4.846153846153846), ("food horrible ", 1.1666666666666667),
                        ("manager nt ", 1.1666666666666667), ("honestly best ", 4.833333333333333),
                        ("sour cherry ", 4.833333333333333), ("wear stretchy ", 4.833333333333333),
                        ("coming time vegas ", 4.833333333333333), ("buffet worth penny ", 4.833333333333333),
                        ("pho dim ", 4.833333333333333), ("hands best buffet ", 4.833333333333333),
                        ("recommend going early ", 4.833333333333333), ("awesome definitely ", 4.833333333333333),
                        ("food fresh hot ", 4.833333333333333), ("wear loose ", 4.833333333333333),
                        ("will leave satisfied ", 4.833333333333333), ("oysters crab claws ", 4.833333333333333),
                        ("fresh raw oysters ", 4.833333333333333), ("seriously best ", 4.833333333333333),
                        ("seafood mexican italian ", 4.833333333333333), ("favorite lamb ", 4.833333333333333),
                        ("definitely pay ", 4.833333333333333)]

        filter_for_completeness(word_ratings)
        filter_words_by_sentiment(word_ratings)
        wordlist = ["room","food","service","location","room","clean"]
        filter_words_by_word2vec_distance(word_ratings,wordlist)
        self.assertNotIn(("horrible customer ", 1.0),word_ratings)
        self.assertNotIn(("http wwwyelpcombizphotosresducsfiiihpdg selectywgfbzxkffoykutq ", 5.0), word_ratings)
        self.assertNotIn(("easily best ", 4.863636363636363), word_ratings)
        self.assertNotIn(("yum yum ", 4.857142857142857), word_ratings)
        self.assertIn(("horrible customer service ", 1.0), word_ratings)
        self.assertIn(("italian dessert ", 5.0), word_ratings)
        print(word_ratings)

def filter_words_by_sentiment(word_ratings, min_difference = 0.2):
    i = 0
    while i<len(word_ratings):
        word_rating = word_ratings[i]
        text = word_rating[0]
        rating = word_rating[1]
        delete_this = True
        for word in text.split():
            sentiment_value = get_senitment_textblob(word) * 4 + 1
            if abs(rating/sentiment_value-1.0) >= min_difference:
                delete_this = False
        if delete_this:
            del word_ratings[i]
        else:
            i += 1

@timing
def filter_words_by_word2vec_distance(word_ratings, word_list, min_distance_one = 0.5, min_distance_all = 0, max_distance = 1):
    cosine = lambda v1, v2: np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    i = 0
    while i<len(word_ratings):
        word_rating = word_ratings[i]
        text = word_rating[0]
        wordvec = detectNLP.get_average_wordvec(text)

        delete_this = False

        min_value = 1
        max_value = 0
        for word in word_list:
            filter_wordvec = detectNLP.get_average_wordvec(word)
            distance = cosine(wordvec,filter_wordvec)
            if distance > max_value:
                max_value = distance
                if max_distance < max_value:
                    delete_this = True
                    break

            if distance < min_value:
                min_value = distance
                if min_value < min_distance_all:
                    delete_this = True
                    break

        if max_value < min_distance_one:
            delete_this = True

        if delete_this:
            del word_ratings[i]
        else:
            i += 1

def filter_for_completeness(word_ratings):
    phrases = []
    for word_rating in word_ratings:
        phrases.append(word_rating[0])

    i = 0
    while i<len(word_ratings):
        word_rating = word_ratings[i]
        text = word_rating[0]
        delete_this = False
        for phrase in phrases:
            if text!=phrase:
                if text in phrase:
                    delete_this = True
                    break
        if delete_this:
            del word_ratings[i]
        else:
            i += 1


if __name__ == '__main__':
    unittest.main()
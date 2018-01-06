import pandas as pd
import ijson
import json, re, csv
from nltk.corpus import wordnet as wn
from googletrans import Translator
import string
import unicodedata
import nltk.stem.snowball as snowball
import nltk
import numpy as np
import tensorflow as tf
import pickle
from xlsxwriter.workbook import Workbook

alphabet = list("abcdefghijklmnopqrstuvwxyz")
en_months = ['jan','january','feb','february','mar','march','apr','april','may','jun','june','jul','julie','aug','august','sept','sep','september','oct','october','nov','november','dec','december']
it_months = ['lunedi','martedi','mercoledi','giovedi','venerdi','sabato','domenica','finesettimana','gennaio','gen','febbraio','marzo','aprile','maggio','mag','giugno','giu','luglio','lug','agosto','ago','settembre','set','ottobre','ott','novembre','dicembre','dic']

stopwords = {
              "en":set(["","a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", "awfully", "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "c", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few", "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "j", "just", "k", "keep	keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "run", "s", "'s", "said", "same", "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure	t", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "x", "y", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "z"] + en_months + alphabet) ,
              "ro":set(["","a", "abia", "acea", "aceasta", "această", "aceea", "aceeasi", "acei", "aceia", "acel", "acela", "acelasi", "acele", "acelea", "acest", "acesta", "aceste", "acestea", "acestei", "acestia", "acestui", "aceşti", "aceştia", "acolo", "acord", "acum", "adica", "ai", "aia", "aibă", "aici", "aiurea", "al", "ala", "alaturi", "ale", "alea", "alt", "alta", "altceva", "altcineva", "alte", "altfel", "alti", "altii", "altul", "am", "anume", "apoi", "ar", "are", "as", "asa", "asemenea", "asta", "astazi", "astea", "astfel", "astăzi", "asupra", "atare", "atat", "atata", "atatea", "atatia", "ati", "atit", "atita", "atitea", "atitia", "atunci", "au", "avea", "avem", "aveţi", "avut", "azi", "aş", "aşadar", "aţi", "b", "ba", "bine", "bucur", "bună", "c", "ca", "cam", "cand", "capat", "care", "careia", "carora", "caruia", "cat", "catre", "caut", "ce", "cea", "ceea", "cei", "ceilalti", "cel", "cele", "celor", "ceva", "chiar", "ci", "cinci", "cind", "cine", "cineva", "cit", "cita", "cite", "citeva", "citi", "citiva", "conform", "contra", "cu", "cui", "cum", "cumva", "curând", "curînd", "când", "cât", "câte", "câtva", "câţi", "cînd", "cît", "cîte", "cîtva", "cîţi", "că", "căci", "cărei", "căror", "cărui", "către", "d", "da", "daca", "dacă", "dar", "dat", "datorită", "dată", "dau", "de", "deasupra", "deci", "decit", "degraba", "deja", "deoarece", "departe", "desi", "despre", "deşi", "din", "dinaintea", "dintr", "dintr-", "dintre", "doar", "doi", "doilea", "două", "drept", "dupa", "după", "dă", "e", "ea", "ei", "el", "ele", "era", "eram", "este", "eu", "exact", "eşti", "f", "face", "fara", "fata", "fel", "fi", "fie", "fiecare", "fii", "fim", "fiu", "fiţi", "foarte", "fost", "frumos", "fără", "g", "geaba", "graţie", "h", "halbă", "i", "ia", "iar", "ieri", "ii", "il", "imi", "in", "inainte", "inapoi", "inca", "incit", "insa", "intr", "intre", "isi", "iti", "j", "k", "l", "la", "le", "li", "lor", "lui", "lângă", "lîngă", "m", "ma", "mai", "mare", "mea", "mei", "mele", "mereu", "meu", "mi", "mie", "mine", "mod", "mult", "multa", "multe", "multi", "multă", "mulţi", "mulţumesc", "mâine", "mîine", "mă", "n", "ne", "nevoie", "ni", "nici", "niciodata", "nicăieri", "nimeni", "nimeri", "nimic", "niste", "nişte", "noastre", "noastră", "noi", "noroc", "nostri", "nostru", "nou", "noua", "nouă", "noştri", "nu", "numai", "o", "opt", "or", "ori", "oricare", "orice", "oricine", "oricum", "oricând", "oricât", "oricînd", "oricît", "oriunde", "p", "pai", "parca", "patra", "patru", "patrulea", "pe", "pentru", "peste", "pic", "pina", "plus", "poate", "pot", "prea", "prima", "primul", "prin", "printr-", "putini", "puţin", "puţina", "puţină", "până", "pînă", "r", "rog", "s", "sa", "sa-mi", "sa-ti", "sai", "sale", "sau", "se", "si", "sint", "sintem", "spate", "spre", "sub", "sunt", "suntem", "sunteţi", "sus", "sută", "sînt", "sîntem", "sînteţi", "să", "săi", "său", "t", "ta", "tale", "te", "ti", "timp", "tine", "toata", "toate", "toată", "tocmai", "tot", "toti", "totul", "totusi", "totuşi", "toţi", "trei", "treia", "treilea", "tu", "tuturor", "tăi", "tău", "u", "ul", "ului", "un", "una", "unde", "undeva", "unei", "uneia", "unele", "uneori", "unii", "unor", "unora", "unu", "unui", "unuia", "unul", "v", "va", "vi", "voastre", "voastră", "voi", "vom", "vor", "vostru", "vouă", "voştri", "vreme", "vreo", "vreun", "vă", "x", "z", "zece", "zero", "zi", "zice", "îi", "îl", "îmi", "împotriva", "în", "înainte", "înaintea", "încotro", "încât", "încît", "între", "întrucât", "întrucît", "îţi", "ăla", "ălea", "ăsta", "ăstea", "ăştia", "şapte", "şase", "şi", "ştiu", "ţi", "ţie"] + en_months + alphabet),
              "it":set(["", "a", "adesso", "ai", "al", "alla", "allo", "allora", "altre", "altri", "altro", "anche", "ancora", "avere", "aveva", "avevano", "ben", "buono", "che", "chi", "cinque", "comprare", "con", "consecutivi", "consecutivo", "cosa", "cui", "da", "de", "del", "della", "dello", "dentro", "deve", "devo", "di", "doppio", "due", "e", "ecco", "fare", "fine", "fino", "fra", "gente", "giu", "ha", "hai", "hanno", "ho", "il", "indietro	invece", "io", "la", "lavoro", "le", "lei", "lo", "loro", "lui", "lungo", "ma", "me", "meglio", "molta", "molti", "molto", "nei", "nella", "no", "noi", "nome", "nostro", "nove", "nuovi", "nuovo", "o", "oltre", "ora", "otto", "peggio", "pero", "persone", "piu", "poco", "primo", "promesso", "qua", "quarto", "quasi", "quattro", "quello", "questo", "qui", "quindi", "quinto", "rispetto", "sara", "secondo", "sei", "sembra	sembrava", "senza", "sette", "sia", "siamo", "siete", "solo", "sono", "sopra", "soprattutto", "sotto", "stati", "stato", "stesso", "su", "subito", "sul", "sulla", "tanto", "te", "tempo", "terzo", "tra", "tre", "triplo", "ultimo", "un", "una", "uno", "va", "vai", "voi", "volte", "vostro"] + en_months + it_months + alphabet),
              }

def replace_diactitics(text):
    text = re.sub("[ăĂâÂ]", "a", text)
    text = re.sub("[îÎ]", "i", text)
    text = re.sub("[șȘ]", "s", text)
    text = re.sub("[țȚ]", "t", text)
    return text

printable = set(string.printable)
def remove_nonprintable(text):
    return list(filter(lambda x: x in printable, text))

def remove_numbers(text):
    return re.sub("[0-9., -]", "", text)

def keep_only_letters(text):
    return re.sub("[^a-z]", "", text)

def keep_only_letters_and_spaces(text):
    return re.sub("[^a-z ]", " ", text)

def replace_review_diactitics(review):
    review["text"] = replace_diactitics(review["text"])

def review_to_ascii(review):
    review["text"] = unicodedata.normalize('NFKD', review["text"]).encode('ascii', 'ignore').decode("ascii")

def review_to_lowered_words(review):
    review["text"] = nltk.word_tokenize(review["text"].lower())

def process_words(text, language=None, stem=True, to_ascii=True, character_level=False):
    if language is None:
        translator = Translator()
        if isinstance(text, list):
            language = translator.detect(text)[0].lang

    if language == "ro":
        if isinstance(text, list):
            text = [replace_diactitics(subtext) for subtext in text]
        else:
            text = replace_diactitics(text)

    if isinstance(text, list):
        if to_ascii:
            text = [ unicodedata.normalize('NFKD', subtext).encode('ascii','ignore').decode("ascii") for subtext in text]
        text = [subtext.lower() for subtext in text]
        words = [nltk.word_tokenize(subtext) for subtext in text]
    else:
        if to_ascii:
            text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').decode("ascii")
        text = text.lower()
        words = nltk.word_tokenize(text)

    procced_text = []

    if language == "ro":
        stemmer = snowball.RomanianStemmer()
    elif language == "it":
        stemmer = snowball.ItalianStemmer()
    elif language == "en":
        stemmer = snowball.EnglishStemmer()
    else:
        stem = False

    stopw = []
    if language in stopwords:
        stopw = stopwords[language]

    if isinstance(text, list):
        for i in range(len(words)):
            sent = words[i]
            sentence = []
            if stem:
                for word in sent:
                    word = keep_only_letters(word)

                    if word not in stopw:
                        if character_level:
                            sentence += list(word)
                        else:
                            sentence.append(stemmer.stem(word))
            else:
                for word in sent:
                    word = keep_only_letters(word)
                    if word not in stopw:
                        if character_level:
                            sentence += list(word)
                        else:
                            sentence.append(word)
            procced_text.append(sentence)
    else:
        for word in words:
            word = keep_only_letters(word)
            if word not in stopw:
                if character_level:
                    procced_text += list(word)
                else:
                    procced_text.append(word)

    return procced_text

def sum_1level_dictionary(dictionary):
    return np.sum(dictionary.values())

def sum_nlevel_dictionary(dictionary, level = 2):
    sum_ = 0
    if level > 1:
        for dict_name in dictionary:
            sum_ += sum_nlevel_dictionary(dictionary[dict_name], level - 1)
    else:
        sum_ = sum_1level_dictionary(dictionary)
    return sum_

def get_top_n(dictionary, n):
    return list(zip(dictionary.keys(), dictionary.values())).sort(key= lambda x:x[1], reverse=True)[:n]

def write_csv(filename, rows):
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"')
        for row in rows:
            csvwriter.writerow(row)

def write_csv_to_xlsx(csv_file):
    workbook = Workbook(csv_file[:-4] + '.xlsx')
    worksheet = workbook.add_worksheet()
    with open(csv_file, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()

def write_csv_and_xlsx(filename, rows):
    if "." not in filename or filename.split(".")[1] != "csv":
        filename = filename.split(".")[0] + ".csv"
    write_csv(filename, rows)
    write_csv_to_xlsx(filename)

#business dict_keys(['business_id', 'name', 'neighborhood', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude', 'stars', 'review_count', 'is_open', 'attributes', 'categories', 'hours'])
#review dict_keys(['review_id', 'user_id', 'business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool'])
#tip dict_keys(['text', 'date', 'likes', 'business_id', 'user_id'])
#photos dict_keys(['photo_id', 'business_id', 'caption', 'label'])
#checkin dict_keys(['time', 'business_id'])
#user dict_keys(['user_id', 'name', 'review_count', 'yelping_since', 'friends', 'useful', 'funny', 'cool', 'fans', 'elite', 'average_stars', 'compliment_hot', 'compliment_more', 'compliment_profile', 'compliment_cute', 'compliment_list', 'compliment_note', 'compliment_plain', 'compliment_cool', 'compliment_funny', 'compliment_writer', 'compliment_photos'])

city2category2count    = dict()
city2business_count    = dict()
business2review_count  = dict()
business_id2categories = dict()
word2rating            = dict()
category2reviews       = dict()
business2reviews_count = dict()
category2reviews_count = dict()
business_id2name       = dict()
business_id2city       = dict()

reviews = []
avg_reviews_for_users = [0.0, 0]
with open(r"dataset\user.json", 'r', encoding='utf-8') as f:
    for line in f:
        j = json.loads(line)
        avg_reviews_for_users[0] += j["review_count"]
        avg_reviews_for_users[1] += 1

print("Average review count for users:",round(avg_reviews_for_users[0]/avg_reviews_for_users[1],5))

with open(r"dataset\business.json", 'r', encoding='utf-8') as f:
    for line in f:
        j = json.loads(line)
        reviews.append(j)
        city = j["city"]
        if city not in city2category2count:
            city2category2count[city] = dict()
            city2business_count[city] = 0
        city2business_count[city] += 1
        categories  = j["categories"]
        business_id = j["business_id"]
        name = j["name"]
        business_id2name[business_id] = name
        business_id2city[business_id] = city
        business_id2categories[business_id] = categories
        business2reviews_count[business_id] = [0] * 5
        for category in categories:
            if category not in category2reviews_count:
                category2reviews_count[category] = [0] * 5

business2word_count = dict()

texts = []
reviews = []
with open(r"dataset\review.json", 'r', encoding='utf-8') as f:
    for line in f:
        review = json.loads(line)
        texts.append(review["text"])
        reviews.append(review)
        business_id = review["business_id"]
        stars = review["stars"]
        business2reviews_count[business_id][stars - 1] += 1
        for category in business_id2categories[business_id]:
            if category not in category2reviews:
                category2reviews[category] = []
            category2reviews[category].append(review)
            category2reviews_count[category][stars - 1] += 1


common_header = []
for i in range(1,6):
    common_header.append(str(i) + " Star Reviews")

common_header.append("Positive Reviews")
common_header.append("Negative Reviews")
common_header.append("All Reviews Count")
common_header.append("Average Rating")

city2reviews_count = dict()
city2businesses    = dict()
for business in business2reviews_count:
    city = business_id2city[business]
    if city not in city2reviews_count:
        city2reviews_count[city] = [0] * 5
        city2businesses[city]    = 0
    city2businesses[city]    += 1
    for k in range(5):
        city2reviews_count[city][k] += business2reviews_count[business][k]

category_rows    = [["Category"] + common_header]
business_id_rows = [["Business Name","Business ID","Number of Categories","Categories","City"] + common_header]
city_rows        = [["City","Businesses" ] + common_header]

for category in category2reviews_count:
    star_counts = category2reviews_count[category]
    row = [category]
    score_sum = 0.0
    for i in range(5):
        score_sum += star_counts[i] * (i+1)
        row.append(star_counts[i])
    row.append(star_counts[3] + star_counts[4])
    row.append(star_counts[0] + star_counts[1])
    number_of_reviews = sum(star_counts)
    row.append(number_of_reviews)
    row.append(score_sum/number_of_reviews)
    category_rows.append(row)

write_csv_and_xlsx("stats/category_stats", category_rows)

for business in business2reviews_count:
    city = business_id2city[business]
    business_name = business_id2name[business]
    categories = business_id2categories[business]
    star_counts = business2reviews_count[business]
    row = [business, business_name, len(categories), categories, city]
    score_sum = 0.0
    for i in range(5):
        score_sum += star_counts[i] * (i+1)
        row.append(star_counts[i])
    row.append(star_counts[3] + star_counts[4])
    row.append(star_counts[0] + star_counts[1])
    number_of_reviews = sum(star_counts)
    row.append(number_of_reviews)
    if number_of_reviews>0:
        row.append(score_sum/number_of_reviews)
    else:
        row.append(0)
    business_id_rows.append(row)

write_csv_and_xlsx("stats/business_stats", business_id_rows)

for city in city2reviews_count:
    star_counts = city2reviews_count[city]
    row = [city, city2businesses[city]]
    score_sum = 0.0
    for i in range(5):
        score_sum += star_counts[i] * (i+1)
        row.append(star_counts[i])
    row.append(star_counts[3] + star_counts[4])
    row.append(star_counts[0] + star_counts[1])
    number_of_reviews = sum(star_counts)
    row.append(number_of_reviews)
    if number_of_reviews>0:
        row.append(score_sum/number_of_reviews)
    else:
        row.append(0)
    city_rows.append(row)

write_csv_and_xlsx("stats/city_stats", city_rows)

import math

split_texts = []
number_of_splits = 100
numuber_of_reviews_per_split = math.ceil(float(len(texts))/number_of_splits)
for i in range(number_of_splits):
    text_chunk = texts[numuber_of_reviews_per_split*i:numuber_of_reviews_per_split*(i+1)]
    text_chunk = process_words(text_chunk, "en", stem=True)
    texts = texts[:numuber_of_reviews_per_split*i] + text_chunk + texts[numuber_of_reviews_per_split*(i+1):]

i = 0
while i < len(texts):
    if texts[i] == []:
        del texts[i]
        del reviews[i]
    else:
        i += 1

for text in texts:
    for word in text:
        if word not in word2rating:
            word2rating[word] = [0.0, 0]
        word2rating[word][1] += 1

frequncy_boundries = [0, 5, 10, 50, 100, 500, 1000, 5000, 10000]
frequency_cnts = [0] * len(frequncy_boundries)

for text in texts:
    for word in text:
        for k, frequncy_boundry in enumerate(frequncy_boundries):
            if word2rating[word][1] >= frequncy_boundry:
                frequency_cnts[k] += 1

for k, frequncy_boundry in enumerate(frequncy_boundries):
    print("Number of words that appear a minimum of", frequncy_boundry,":",frequency_cnts[k])

MIN_DOCUMENT_LENGTH = 10000000
MAX_DOCUMENT_LENGTH = 0
word_total = 0.0
for text in texts:
    length = len(text)
    if length > MAX_DOCUMENT_LENGTH:
        MAX_DOCUMENT_LENGTH = length
    if length < MIN_DOCUMENT_LENGTH:
        MIN_DOCUMENT_LENGTH = length
    word_total += length
print("Average number of words per review:",word_total/len(texts))
print("Min number of words:", MIN_DOCUMENT_LENGTH)
print("Max number of words:", MAX_DOCUMENT_LENGTH)


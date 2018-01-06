import heapq
import numpy as np
from data_helpers import *

def build_confusion_matrix(labels, predicted_labels, label2num = None):
    if label2num == None:
        label2num = dict()
        for label in labels:
            if isinstance(label, list):
                for sublabel in label:
                    if sublabel not in label2num and sublabel != '':
                        label2num[sublabel] = len(label2num)
            elif label not in label2num:
                label2num[label] = len(label2num)
        for label in predicted_labels:
            if isinstance(label, list):
                for sublabel in label:
                    if sublabel not in label2num and sublabel != '':
                        label2num[sublabel] = len(label2num)
            elif label not in label2num:
                label2num[label] = len(label2num)

    confusion = np.zeros((len(label2num), len(label2num)))
    for i in range(len(labels)):
        label = labels[i]
        predicted_label = predicted_labels[i]
        if isinstance(label, list):
            for sublabel in label:
                if predicted_label in label2num and sublabel != '':
                    confusion[label2num[sublabel]][label2num[predicted_label]] += 1
        else:
            confusion[label2num[label]][label2num[predicted_label]] +=1

    return confusion, label2num

def write_confusion_matrix(labels, predicted_labels, name, as_percentage = False, label2num = None):
    confusion, label2num = build_confusion_matrix(labels, predicted_labels, label2num)

    row = [''] * (len(label2num) + 1)
    for label in label2num:
        num = label2num[label] + 1
        row[label2num[label] + 1] = label

    rows = [row]
    number2label = dict(zip(label2num.values(), label2num.keys()))

    if as_percentage:
        for i in range(len(confusion)):
            row_sum = np.sum(confusion[i])
            row = [number2label[i]]
            for j in range(len(confusion[i])):
                row.append(to_percentage(float(confusion[i][j])/row_sum))
            rows.append(row)
    else:
        for i in range(len(confusion)):
            row_sum = np.sum(confusion[i])
            row = [number2label[i]]
            for j in range(len(confusion[i])):
                row.append(confusion[i][j])
            rows.append(row)

    filename = ''
    if name[:5] != 'data/' :
        filename += 'data/'
    if name[len(name)-4:] != '.csv':
        filename += name + '.csv'
    else:
        filename += name

    write_csv( filename, rows)
    write_csv_to_xlsx(filename)

def to_percentage(x):
    return str(round(x*100, 2))+"%"

def to_num(x):
    if isinstance(x, str):
        if x[-1] == '%':
            return round(float(x[:-1]) / 100, 5)
        else:
            return float(x)
    return x

def get_top(a, k=5):
    if a is np.ndarray:
        return heapq.nlargest(k, range(len(a)), a.take)
    else:
        return heapq.nlargest(k, range(len(a)), a.__getitem__)

if __name__ == "__main__":
    import csv
    encoding = "utf-8"
    word2word2vec = dict()
    word2GloVe    = dict()
    with open("data/category_trainedWord2vec-KMeans-Food_word2cluster.csv", 'r') as f:
        reader = csv.reader(f)
        skip = True
        for row in reader:
            if skip:
                skip = False
            else:
                word2word2vec[row[0]] = row[1]

    with open("data/GloVe-KMeans-Food_word2cluster.csv", 'r') as f:
        reader = csv.reader(f)
        skip = True
        for row in reader:
            if skip:
                skip = False
            else:
                word2GloVe[row[0]] = row[1]

    words = []
    word2vecClusters = []
    GloVeClusters = []
    for word in word2word2vec:
        words.append(word)
        word2vecClusters.append(word2word2vec[word])
        GloVeClusters.append(word2GloVe[word])

    write_confusion_matrix(word2vecClusters, GloVeClusters, "word2vecVsGloVe-ConfusionMatrix")

    
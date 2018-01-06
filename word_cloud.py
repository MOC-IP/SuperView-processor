from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

def make_word_cloud(text, output_file, mask_file = "images/hotel3.jpg", show = False):
    mask = np.array(Image.open(mask_file))

    stopwords = set(STOPWORDS)

    wc = WordCloud(background_color="white", max_words=2000, mask=mask,
                   stopwords=stopwords)
    # generate word cloud
    wc.generate(text)

    # store to file
    wc.to_file( output_file)

    if show:
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.figure()
        plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    d = path.dirname(__file__)

    # Read the whole text.
    text = open(path.join(d, 'SentimentAnalysis.py')).read()

    # read the mask image
    # taken from
    # http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
    mask = np.array(Image.open(path.join(d, "images/hotel3.jpg")))

    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(background_color="white", max_words=2000, mask=mask,
                   stopwords=stopwords)
    # generate word cloud
    wc.generate(text)

    # store to file
    wc.to_file(path.join(d, "images/hotel_word_cloud.png"))

    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.show()
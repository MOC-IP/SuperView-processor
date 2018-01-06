# SuperView-processor

## This part of the project includes the following components accessed through an API build through Flask:
- ### Topic analysis on a business
  Accessed through the following path:
  /api/topics/all/<string:business_id>
  It uses scikit-learn's [Latent Dirichlet allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) and [Non-negative matrix factorization](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html) to form topics based on a business's positive and negative reviews, thus forming topics that describe the negative aspects of the hotel and the positive aspects of the hotel
- ### Bigram and Trigram Extraction
  Accessed through the following path:
  /api/phrasees/all/<string:business_id>
  It looks at all bigrams and trigrams (2-word and 3-word groups) and calculated the average rating for each one it then filters the phrases in the following ways:
  - it removes bigrams that are contained in trigrams
  - it removes phrases that don't appear a certain number of times (default 5)
  - it removes phrases that are not close enough to a set of words based on word2vec, this is done to remove phrases that are not relevent to custumers
  - it aplies sentiment analysis and removes phrases whoose average score matches the sentiment score, this is done to only show phrases for which their score contains inportant information
- ### Adjective and Noun Pair Extraction
  Accessed through the following path:
  /api/phrasees/noun_adj/<string:business_id>
  It uses Spacy's dependency parser to evaluate dependencies in each review and extract the lematized version of nouns and adjectives which have a dependency between them and calculates their average score. It removes the phrases that don't appear a certain number of times (default 5) and sorts the remaining phrases in descending order based on how far they are from the neutral rating ( in Yelp 3 stars).
  
 ## This repository also contains the fllowing:
  - The SentimentAnalysis module contains code for using and comparing 3 sentiment analysis libraries (Vader through NLTK, Stanford CoreNLP and TextBlob)
  - The data_functions module contains functions for extracting data through MongoDB
  - The word2vecClurstering module uses category trained Word2vec and GloVe and pretrained Word2vec (trained by Spacy on the Common Crawl) to clurster using KMeans, DBSCAN, and GaussianMixtures, and forms wordclouds based on these clusters
  - The wordnet module contains a Wordnet interface that can extract synonyms and hypernyms, paired with a module that can find the common root word or words based on a maximum distance in the Wordnet graph
  - The addBias module calculatates bias for reviews based on average rating of the business category, the user reviews and the business reviews using the methodology resulted from the [Netflix Prize](http://blog.echen.me/2011/10/24/winning-the-netflix-prize-a-summary/) in 2009.
  - The coherence module tests topic coherence using [Gensim topic coherence function](https://radimrehurek.com/gensim/models/coherencemodel.html), the methodology is based on [a study made by Michael Roeder, Andreas Both and Alexander Hinneburg](http://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)
  - The ylp fusion API module is an interface to the Yelp Fusion API

# Text preprocessing
import numpy as np
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

stemmer = PorterStemmer()

def preprocess_text(text):
    # Lowercasing
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenization
    words = nltk.word_tokenize(text)

    # # Remove stopwords
    # words = [w for w in words if w not in stopwords.words('english')]

    # Stemming
    words = [stemmer.stem(w) for w in words]

    return words

# BOW implementation
def bag_of_words(tokenized_sentence, words):
    # stem each word
    sentence_words = [word for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag


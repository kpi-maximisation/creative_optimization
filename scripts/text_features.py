import pandas as pd
from nltk.corpus import stopwords
from wordcloud import STOPWORDS, WordCloud
import numpy as np
import string
import os
import re
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import operator


def preprocess_first(text):
    # Remove the stop words to prepare the word clouds
    stopWords = set(STOPWORDS)
    # stopWords.update(["RT","https","will","the"])

    # Regex patterns
    urlPattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern = '@[^\s]+'
    sequencePattern = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"

    # Replace 3 or more consecutive letters by 2 letter.
    text = text.replace('[^a-zA-Z\s]', ' ')
    #     /^[a-zA-Z\s]*$/g
    text =' '.join(
        re.sub(sequencePattern, seqReplacePattern, word) for word in text.split())
    # remove characters and non-english letters

    return text


def sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)["compound"]


def text_features(text, game_id):
    audio_dict = {}
    audio_dict['game_id'] = game_id
    audio_dict['text'] = text
    # audio_dict['clean_text'] = preprocess_first(text)
    audio_dict['sentiment_score'] = sentiment(audio_dict['text'])
    score = audio_dict['sentiment_score']
    audio_dict['sentiment'] =  np.select([score<0, score==0, score>0],['negative','neutral','positive'])
    audio_dict['word_count'] = str(len(audio_dict['text'].split()))

    df_text = pd.DataFrame.from_dict([audio_dict])
    return df_text

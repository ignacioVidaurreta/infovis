import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import requests

import matplotlib.pyplot as plt

def update_dict(current_dict, words):
    for word in words:
        normalized = word.upper()
        if normalized in current_dict:
            current_dict[normalized] = current_dict[normalized] + 1
        else:
            current_dict[normalized] = 1

    return current_dict



with open("links.txt", "r") as f:
    links = f.readlines()
    links = [ l.rstrip() for l in links] # Remove trailing newline

word_dict = {}
for link in links:
    data = requests.get(link).content.decode() # We need to convert bytearray to string
    words = data.split("\n") # Get words
    word_dict = update_dict(word_dict, words)

# print(word_dict)
wordcloud = WordCloud(background_color=None, mode='RGBA', width=1000, height=1000, max_words=30, relative_scaling=0.5, normalize_plurals=True).generate_from_frequencies(word_dict)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
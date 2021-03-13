import re
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import requests
import matplotlib.pyplot as plt
# Cool resource: https://towardsdatascience.com/simple-wordcloud-in-python-2ae54a9f58e5

_RE_COMBINE_WHITESPACES = re.compile(r"\s+")

def normalize_word(line):
    return _RE_COMBINE_WHITESPACES.sub(" ", line.replace("-", " ")).strip().upper()

def update_dict(current_dict, words):
    for word in words:
        normalized = normalize_word(word)
        if normalized != '':
            if normalized in current_dict:
                current_dict[normalized] = current_dict[normalized] + 1
            else:
                current_dict[normalized] = 1

    return current_dict


with open("links.txt", "r") as f:
    links = f.readlines()
    links = [l.rstrip() for l in links] # Remove trailing newline

word_dict = {}
for link in links:
    data = requests.get(link).content.decode() # We need to convert bytearray to string
    words = data.split("\n") # Get words
    word_dict = update_dict(word_dict, words)

mask = np.array(Image.open('../media/comment_mask.png'))
print(dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True)))
wc = WordCloud(width=4000, height=3000, random_state=1, max_words=70,
                      background_color='black', colormap='Pastel1', collocations=False,
                      stopwords=STOPWORDS, normalize_plurals=True, mask=mask
                      ).generate_from_frequencies(word_dict)
# plt.axis("off")
# plt.figure(figsize=(50, 40))
# # plt.imshow(wordcloud, interpolation='bilinear')
wc.to_file("../media/word_cloud.jpg")

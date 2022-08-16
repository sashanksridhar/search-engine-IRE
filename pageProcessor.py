from Stemmer import Stemmer
import re
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

class PageProcessor():

    def __init__(self):
        self.stemmer = Stemmer('english')
        self.stop_words = list(stopwords.words('english'))

    def title_processing(self, title_string):

        title_frequency = defaultdict(int)

        total_toks = len(re.findall(r'\w+', title_string))

        title_string = re.sub('\\b[-\.]\\b', '', title_string)
        title_string = re.sub('[^A-Za-z0-9\{\}\[\]\=]+', ' ', title_string)
        for each_word in wordpunct_tokenize(title_string):
            if each_word.isnumeric():
                continue
            each_word = each_word.lower()
            if each_word not in self.stop_words:
                each_word = self.stemmer.stemWord(each_word)
                title_frequency[each_word] += 1

        return title_frequency, total_toks, len(title_frequency.keys())

    def text_processing(self, text_string):

        total_toks = 0

        text_string = re.sub('[^A-Za-z0-9\{\}\[\]\=]+',' ', text_string)
        text_frequency = defaultdict(int)

        regex_category = re.compile(r'\[\[Category(.*?)\]\]')
        table = str.maketrans(dict.fromkeys('\{\}\=\[\]'))
        new_text = regex_category.split(text_string)
        if len(new_text) > 1:
            for text in new_text[1:]:

                text = text.translate(table)
                for word in wordpunct_tokenize(text):
                    total_toks+=1
                    if word.isnumeric():
                        continue
                    word = word.lower()
                    stemmed_term = self.stemmer.stemWord(word)
                    if stemmed_term in self.stop_words or stemmed_term == '':
                        continue
                    if stemmed_term not in text_frequency:
                        text_frequency[stemmed_term] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
                    text_frequency[stemmed_term]['c'] += 1
            text_string = new_text[0]

        new_text = text_string.split('==External links==')
        if len(new_text) > 1:
            new_text[1] = new_text[1].translate(table)

            for word in wordpunct_tokenize(new_text[1]):
                total_toks+=1
                if word.isnumeric():
                    continue
                word = word.lower()
                stemmed_term = self.stemmer.stemWord(word)
                if stemmed_term in self.stop_words or stemmed_term == '':
                    continue

                if stemmed_term not in text_frequency:
                    text_frequency[stemmed_term] = dict(t=0,b=0,i=0,c=0,l=0,r=0)

                text_frequency[stemmed_term]['l'] += 1

            text_string = new_text[0]

        new_text = text_string.split("{{Infobox")

        braces_count = 1
        default_tag_type = 'i'

        if len(new_text) > 1:
            new_text[0] = new_text[0].translate(table)
            for word in wordpunct_tokenize(new_text[0]):
                total_toks+=1
                if word.isnumeric():
                    continue
                word = word.lower()
                stemmed_term = self.stemmer.stemWord(word)
                if stemmed_term in self.stop_words or stemmed_term == '':
                    continue
                if stemmed_term not in text_frequency:
                    text_frequency[stemmed_term] = dict(t=0,b=0,i=0,c=0,l=0,r=0)

                text_frequency[stemmed_term]['b'] += 1

            for word in re.split(r"[^A-Za-z0-9]+",new_text[1]):
                total_toks+=1
                word = word.lower()
                if word.isnumeric():
                    continue

                if "}}" in word.lower():
                    braces_count -= 1
                if "{{" in word.lower():
                    braces_count += 1
                    continue
                if braces_count == 0:
                    default_tag_type = 'b'
                word = word.lower().translate(table)
                stemmed_term = self.stemmer.stemWord(word)
                if stemmed_term in self.stop_words or stemmed_term == '':
                    continue
                if stemmed_term not in text_frequency:
                    text_frequency[stemmed_term] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
                text_frequency[stemmed_term][default_tag_type] += 1
        else:
            text_string = text_string.translate(table)
            for word in wordpunct_tokenize(text_string):
                total_toks+=1
                word = word.lower()
                if word.isnumeric():
                    continue
                stemmed_term = self.stemmer.stemWord(word)
                if stemmed_term in self.stop_words or stemmed_term == '':
                    continue
                if stemmed_term not in text_frequency:
                    text_frequency[stemmed_term] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
                text_frequency[stemmed_term]['b'] += 1

        return text_frequency, total_toks, len(text_frequency.keys())
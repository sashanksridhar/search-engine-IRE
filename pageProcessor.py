from Stemmer import Stemmer
import re
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

class PageProcessor():

    def __init__(self):
        self.stemmer = Stemmer('english')
        self.stop_words = list(stopwords.words('english'))

    def processing(self, word):
        if word.isnumeric():
            return ''
        word = word.lower()
        if word in self.stop_words:
            return ''
        stemmed_term = self.stemmer.stemWord(word)
        return stemmed_term

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
        words_set, body_dict, category_dict, infobox_dict, link_dict = set(), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)

        regex_category = re.compile(r'\[\[Category(.*?)\]\]')
        table = str.maketrans(dict.fromkeys('\{\}\=\[\]'))

        new_text = regex_category.split(text_string)
        if len(new_text) > 1:
            for text in new_text[1:]:

                text = text.translate(table)
                for word in wordpunct_tokenize(text):
                    total_toks+=1
                    stemmed_term = self.processing(word)
                    if stemmed_term == '':
                        continue
                    words_set.update([stemmed_term])
                    category_dict[stemmed_term] += 1
            text_string = new_text[0]

        new_text = text_string.split('==External links==')
        if len(new_text) > 1:
            new_text[1] = new_text[1].translate(table)

            for word in wordpunct_tokenize(new_text[1]):
                total_toks+=1
                stemmed_term = self.processing(word)
                if stemmed_term == '':
                    continue

                words_set.update([stemmed_term])
                link_dict[stemmed_term] += 1

            text_string = new_text[0]

        new_text = text_string.split("{{Infobox")

        braces_count = 1
        default_tag_type = 'i'

        if len(new_text) > 1:
            new_text[0] = new_text[0].translate(table)
            for word in wordpunct_tokenize(new_text[0]):
                total_toks+=1
                stemmed_term = self.processing(word)
                if stemmed_term == '':
                    continue
                words_set.update([stemmed_term])
                body_dict[stemmed_term] += 1

            for word in re.split(r"[^A-Za-z0-9]+",new_text[1]):
                total_toks+=1

                if "}}" in word.lower():
                    braces_count -= 1
                if "{{" in word.lower():
                    braces_count += 1
                    continue
                if braces_count == 0:
                    default_tag_type = 'b'
                stemmed_term = self.processing(word.lower().translate(table))
                if stemmed_term == '':
                    continue
                words_set.update([stemmed_term])
                if default_tag_type == 'b':
                    body_dict[stemmed_term] += 1
                else:
                    infobox_dict[stemmed_term] += 1
        else:
            text_string = text_string.translate(table)
            for word in wordpunct_tokenize(text_string):
                total_toks+=1
                stemmed_term = self.processing(word)
                if stemmed_term == '':
                    continue
                words_set.update([stemmed_term])
                body_dict[stemmed_term] += 1

        return words_set, body_dict, category_dict, infobox_dict, link_dict, total_toks, len(words_set)
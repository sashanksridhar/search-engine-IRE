from Stemmer import Stemmer
import re
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords

class PageProcessor():

    def __init__(self):
        self.stemmer = Stemmer('english')
        self.stop_words = list(stopwords.words('english'))

    def title_processing(self, title_string):

        title_frequency = dict()

        total_toks = len(re.findall(r'\w+', title_string))

        title_string = re.sub('\\b[-\.]\\b', '', title_string)
        title_string = re.sub('[^A-Za-z0-9\{\}\[\]\=]+', ' ', title_string)
        for each_word in wordpunct_tokenize(title_string):
            # each_word = each_word.lower()
            if each_word.lower() not in self.stop_words:
                each_word = self.stemmer.stemWord(each_word.lower())
                if each_word not in title_frequency:
                    title_frequency[each_word] = 0
                title_frequency[each_word] += 1

        return title_frequency, total_toks, len(title_frequency.keys())

    def text_processing(self, text_string):

        total_toks = 0

        text_string = re.sub('[^A-Za-z0-9\{\}\[\]\=]+',' ', text_string)
        text_frequency = dict()

        regex_category = re.compile(r'\[\[Category(.*?)\]\]')
        table = str.maketrans(dict.fromkeys('\{\}\=\[\]'))
        new_text = regex_category.split(text_string)
        if len(new_text) > 1:
            for text in new_text[1:]:
                text = text.translate(table)
                for word in wordpunct_tokenize(text):
                    total_toks+=1
                    # word = word.lower()
                    if word.lower() not in text_frequency:
                        text_frequency[word.lower()] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
                    text_frequency[word.lower()]['c'] += 1
            text_string = new_text[0]

        new_text = text_string.split('==External links==')
        if len(new_text) > 1:
            new_text[1] = new_text[1].translate(table)

            for word in wordpunct_tokenize(new_text[1]):
                total_toks+=1
                # word = word.lower()
                if word.lower() not in text_frequency:
                    text_frequency[word.lower()] = dict(t=0,b=0,i=0,c=0,l=0,r=0)

                text_frequency[word.lower()]['l'] += 1

            text_string = new_text[0]

        new_text = text_string.split("{{Infobox")

        braces_count = 1
        default_tag_type = 'i'

        if len(new_text) > 1:
            new_text[0] = new_text[0].translate(table)
            for word in wordpunct_tokenize(new_text[0]):
                total_toks+=1
                # word = word.lower()
                if word.lower() not in text_frequency:
                    text_frequency[word.lower()] = dict(t=0,b=0,i=0,c=0,l=0,r=0)

                text_frequency[word.lower()]['b'] += 1

            for word in re.split(r"[^A-Za-z0-9]+",new_text[1]):
                total_toks+=1
                word = word.lower()
                if "}}" in word.lower():
                    braces_count -= 1
                if "{{" in word.lower():
                    braces_count += 1
                    continue
                if braces_count == 0:
                    default_tag_type = 'b'
                word = word.lower().translate(table)

                if word not in text_frequency:
                    text_frequency[word] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
                text_frequency[word][default_tag_type] += 1
        else:
            text_string = text_string.translate(table)
            for word in wordpunct_tokenize(text_string):
                total_toks+=1
                word = word.lower()

                if word.lower() not in text_frequency:
                    text_frequency[word.lower()] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
                text_frequency[word.lower()]['b'] += 1

        duplicate_copy = dict()
        for term in text_frequency:
            stemmed_term = self.stemmer.stemWord(term)
            if stemmed_term not in duplicate_copy:
                duplicate_copy[stemmed_term] = text_frequency[term]
            else:
                for key in duplicate_copy[stemmed_term]:
                    duplicate_copy[stemmed_term][key] += text_frequency[term][key]

        text_frequency = dict()
        for term in duplicate_copy:
            if term not in self.stop_words or term != '':
                text_frequency[term] = duplicate_copy[term]

        return text_frequency, total_toks, len(text_frequency.keys())
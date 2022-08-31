from Stemmer import Stemmer
import re
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import defaultdict


class PageProcessor():

    def __init__(self, hindi_indexer):

        self.hindi_indexer = hindi_indexer
        if self.hindi_indexer:
            with open('hindi_stem_words.txt', 'r', encoding='utf-8') as f:
                self.stem_words = [word.strip() for word in f]
            with open('hindi_stopwords.txt', 'r', encoding='utf-8') as f:
                self.stop_words = [word.strip() for word in f]
        else:
            # Stemmer
            self.stemmer = Stemmer('english')
            # List of stop words
            self.stop_words = list(stopwords.words('english'))

    def stem_word(self, word):
        for wrd in self.stem_words:
            if word.endswith(wrd):
                word = word[:-len(wrd)]
                return word
        return word

    def title_processing(self, title_string):

        # Title Frequency Dictionary
        title_dict = defaultdict(int)

        # Find all words
        total_toks = len(re.findall(r'\w+', title_string))
        title_string = re.sub('\\b[-\.]\\b', '', title_string)

        if not self.hindi_indexer:
            title_string = re.sub('[^A-Za-z0-9\{\}\[\]\=]+', ' ', title_string)
        if self.hindi_indexer:
            tokens = title_string.split()
        else:
            tokens = wordpunct_tokenize(title_string)

        # Tokenize
        for each_word in tokens:
            if each_word.isnumeric():
                continue
            if each_word.lower() not in self.stop_words:

                # Stem Word
                if self.hindi_indexer:
                    each_word = self.stem_word(each_word.lower())
                else:
                    each_word = self.stemmer.stemWord(each_word.lower())
                title_dict[each_word] += 1

        return title_dict, total_toks, len(title_dict.keys())

    # Body Processing
    def text_processing(self, text_string):

        # Token Counter for the page
        total_toks = 0

        if not self.hindi_indexer:
            text_string = re.sub('[^A-Za-z0-9\{\}\[\]\=]+', ' ', text_string)



        # Frequency of Page objects
        # {category, link, infobox, body}
        text_frequency = dict()

        # Category
        regex_category = re.compile(r'\[\[Category(.*?)\]\]')
        table = str.maketrans(dict.fromkeys('\{\}\=\[\]'))
        new_text = regex_category.split(text_string)
        if len(new_text) > 1:
            for text in new_text[1:]:
                text = text.translate(table)
                if self.hindi_indexer:
                    tokens = text.split()
                else:
                    tokens = wordpunct_tokenize(text)
                for word in tokens:
                    total_toks += 1
                    if word.isnumeric():
                        continue
                    # word = word.lower()
                    if word.lower() not in text_frequency:
                        text_frequency[word.lower()] = dict(t=0, b=0, i=0, c=0, l=0, r=0)
                    text_frequency[word.lower()]['c'] += 1
            text_string = new_text[0]

        # Links
        new_text = text_string.split('==External links==')
        if len(new_text) > 1:
            new_text[1] = new_text[1].translate(table)

            if self.hindi_indexer:
                tokens = new_text[1].split()
            else:
                tokens = wordpunct_tokenize(new_text[1])

            for word in tokens:
                total_toks += 1
                if word.isnumeric():
                    continue
                # word = word.lower()
                if word.lower() not in text_frequency:
                    text_frequency[word.lower()] = dict(t=0, b=0, i=0, c=0, l=0, r=0)

                text_frequency[word.lower()]['l'] += 1

            text_string = new_text[0]

        # References
        new_text = text_string.split('==References==')

        if len(new_text) > 1:
            new_text[1] = new_text[1].translate(table)

            if self.hindi_indexer:
                tokens = new_text[1].split()
            else:
                tokens = wordpunct_tokenize(new_text[1])

            for word in tokens:
                total_toks += 1
                if word.isnumeric():
                    continue
                # word = word.lower()
                if word.lower() not in text_frequency:
                    text_frequency[word.lower()] = dict(t=0, b=0, i=0, c=0, l=0, r=0)

                text_frequency[word.lower()]['r'] += 1

            text_string = new_text[0]

        # Infobox
        new_text = text_string.split("{{Infobox")

        braces_count = 1
        default_tag_type = 'i'

        if len(new_text) > 1:
            new_text[0] = new_text[0].translate(table)
            if self.hindi_indexer:
                tokens = new_text[0].split()
            else:
                tokens = wordpunct_tokenize(new_text[0])

            for word in tokens:
                total_toks += 1
                if word.isnumeric():
                    continue
                # word = word.lower()
                if word.lower() not in text_frequency:
                    text_frequency[word.lower()] = dict(t=0, b=0, i=0, c=0, l=0, r=0)

                text_frequency[word.lower()]['b'] += 1

            for word in re.split(r"[^A-Za-z0-9]+", new_text[1]):
                total_toks += 1
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

                if word not in text_frequency:
                    text_frequency[word] = dict(t=0, b=0, i=0, c=0, l=0, r=0)
                text_frequency[word][default_tag_type] += 1
        else:
            text_string = text_string.translate(table)
            if self.hindi_indexer:
                tokens = text_string.split()
            else:
                tokens = wordpunct_tokenize(text_string)

            for word in tokens:
                total_toks += 1
                word = word.lower()
                if word.isnumeric():
                    # print("yes")
                    continue
                if word.lower() not in text_frequency:
                    text_frequency[word.lower()] = dict(t=0, b=0, i=0, c=0, l=0, r=0)
                text_frequency[word.lower()]['b'] += 1

        duplicate_copy = dict()
        for term in text_frequency:
            if self.hindi_indexer:
                stemmed_term = self.stem_word(term)
            else:
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
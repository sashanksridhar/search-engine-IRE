import re
from nltk.corpus import stopwords
STOP_WORDS = list(stopwords.words('english'))

references_re = re.compile(u"={2,3} ?references ?={2,3}.*?={2,3}", re.DOTALL)
external_links_re = re.compile(u"={2,3} ?external links?={2,3}.*?\n\n", re.DOTALL)
category_re = re.compile(u"\[\[category:.*?\]\]", re.DOTALL)
infobox_re = re.compile(u"\{\{infobox.*?\}\}", re.DOTALL)
url_re = re.compile(u"((http[s]?:\/\/)|(www\.))(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
number_re = re.compile(u"(\d+\,?)+(\.)?\d+")


UNNECESSARY = ["access", "first", "title", "url", "date", "publisher", "last", "location", "cite", "web", "book", "article", "author", "year", "isbn", "ref", "editor", "volume", "issue"]


REFERENCES_SUB = "(={2,3} ?[rR]eferences ?={2,3})|(={2,3})|" + "|".join(UNNECESSARY)

# Extra noise
NOISE = u".,|+-@~`:;?()*\"'=\\&/<>[]{}#!%^$ "

# Noise filter | Making this dictionary to improve time
NOISE_FILTER = {}
# Strip with these punctuation symbols while tokenization
PUNCTUATION = [u".", u",", u"|", u"-", u":", u";", u"?", u"(", u")", u"*", u"\"", u"\'", u"=", u'\\', u"&", u'/', u"<", u">", u"[", u"]", u"{", u"}", u"#", u"!", u"%"]

filters = STOP_WORDS + PUNCTUATION + UNNECESSARY
for stop_word in filters:
    word = stop_word.strip()
    NOISE_FILTER[word] = 1

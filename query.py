import re
from nltk.corpus import stopwords
from Stemmer import Stemmer

def query_processing(query):
    stemmer = Stemmer('english')
    stop_words = list(stopwords.words('english'))
    queries = dict()
    # field_reg = re.compile(r'[a-z]+:[A-Za-z0-9]+[ ]?')
    field_list = ['title:', 'body:','category:','infobox','ref:']
    query = query.lower()
    field_reg = re.finditer('(title:|infobox:|body:|category:|ref:)([\w+\s+]+)(?=(title:|infobox:|body:|category:|ref:|$))',query)
    if any(1 for field in field_list if field in query):
		#query_regex = field_reg.findall(query)
		# print("query_regex :", query_regex)
        for elem in field_reg:
            term = elem.group(0).split(":")
            #print(term)
            try:
                term_list = list(stemmer.stemWord(word.lower()) for word in term[1].split() if word not in stop_words)
                for t in term_list:
                    queries[term[0]].append(t)
            except KeyError:
                queries[term[0]] = list(stemmer.stemWord(word.lower()) for word in term[1].split() if word not in stop_words)
    else:
        words = query.strip().split(' ')
        try:
            term_list = list(stemmer.stemWord(word.lower()) for word in words if word not in stop_words)
            for t in term_list:
                queries['all'].append(t)
        except KeyError:
            queries['all'] = list(stemmer.stemWord(word.lower()) for word in words if word not in stop_words)

    return queries
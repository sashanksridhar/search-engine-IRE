import re
from nltk.corpus import stopwords
from Stemmer import Stemmer


def mapping_shortform(field):
    field = field.lower()

    if field == "title":
        return "t"
    elif field == "infobox":
        return "i"
    elif field == "category":
        return "c"
    elif field == "body":
        return "b"
    elif field == "ref":
        return "b"
    else:
        return field

def query_processing(query):
    stemmer = Stemmer('english')
    stop_words = list(stopwords.words('english'))
    queries = dict()
    # field_reg = re.compile(r'[a-z]+:[A-Za-z0-9]+[ ]?')

    query = query.lower()
    # field_reg = re.finditer('(t:|i:|b:|c:|r:)([\w+\s+]+)(?=(t:|i:|b:|c:|r:|$))',query)
    if ":" in query:
        query_bag = query.split(" ")
        for q in query_bag:
            field_query = q.split(":")
            field = field_query[0]
            query = field_query[1]
            field = mapping_shortform(field)
            query_words = query.split()

            #print(term)
            try:
                term_list = list(stemmer.stemWord(word.lower()) for word in query_words if word not in stop_words)
                for t in term_list:
                    queries[field].append(t)
            except KeyError:
                queries[field] = list(stemmer.stemWord(word.lower()) for word in query_words if word not in stop_words)
    else:
        words = query.strip().split(' ')
        try:
            term_list = list(stemmer.stemWord(word.lower()) for word in words if word not in stop_words)
            for t in term_list:
                queries['all'].append(t)
        except KeyError:
            queries['all'] = list(stemmer.stemWord(word.lower()) for word in words if word not in stop_words)

    return queries
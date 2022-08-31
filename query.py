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

def stem_word(word, stem_words):
	for wrd in stem_words:
		if word.endswith(wrd):
			word = word[:-len(wrd)]
			return word
	return word

def query_processing(query, hindi_query=False):
    if hindi_query:
        with open('hindi_stopwords.txt', 'r') as f:
            stop_words = [word.strip() for word in f]
        with open('hindi_stem_words.txt', 'r') as f:
            stem_words = [word.strip() for word in f]
    else:
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
                if hindi_query:
                    term_list = list(stem_word(word.lower(), stem_words) for word in query_words if word not in stop_words)
                else:
                    term_list = list(stemmer.stemWord(word.lower()) for word in query_words if word not in stop_words)
                for t in term_list:
                    queries[field].append(t)
            except KeyError:
                if hindi_query:
                    queries[field] = list(
                        stem_word(word.lower(), stem_words) for word in query_words if word not in stop_words)
                else:
                    queries[field] = list(stemmer.stemWord(word.lower()) for word in query_words if word not in stop_words)
    else:
        words = query.strip().split(' ')
        try:
            if hindi_query:
                term_list = list(stem_word(word.lower(), stem_words) for word in words if word not in stop_words)
            else:
                term_list = list(stemmer.stemWord(word.lower()) for word in words if word not in stop_words)
            for t in term_list:
                queries['all'].append(t)
        except KeyError:
            if hindi_query:
                queries['all'] = list(stem_word(word.lower(), stem_words) for word in words if word not in stop_words)
            else:
                queries['all'] = list(stemmer.stemWord(word.lower()) for word in words if word not in stop_words)

    return queries
import Stemmer
import re
from nltk.corpus import stopwords

stemmer = Stemmer.Stemmer('english')
stop_words = set(stopwords.words('english'))


def tokenize(data):
	data = data.encode("ascii", errors="ignore").decode()
	data = re.sub(r'http[^\ ]*\ ', r' ', data)  # removing urls
	data = re.sub(r'&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;', r' ', data)  # removing html entities
	data = re.sub(
		r'\—|\%|\$|\'|\||\.|\*|\[|\]|\:|\;|\,|\{|\}|\(|\)|\=|\+|\-|\_|\#|\!|\`|\"|\?|\/|\>|\<|\&|\\|\u2013|\n', r' ',
		data)  # removing special characters
	data = re.sub(r'\d', '', data).strip()
	return data.split()

def make_lower(data):
	return data.lower()

def stem_and_stop(tokens):
	stemmed = [stemmer.stemWord(word) for word in tokens if stemmer.stemWord(word) not in stop_words]
	return stemmed


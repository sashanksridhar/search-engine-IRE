#!/bin/sh
pip install -r requirements.txt
python -m nltk.downloader stopwords

python indexer.py $1 $2 $3
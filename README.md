# Wikipedia Search Engine

### Prerequisites
1. Python3
2. nltk
3. PyStemmer

### Datasets

[Download Sample Dataset](https://drive.google.com/file/d/1tknEB9yt2AXNKJp3UvJoNRyfiTh-Nzpr/view) 

[Download 90 GB Dataset](https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/20220820/enwiki-20220820-pages-articles-multistream.xml.bz2) 

[Download Code Mix Dataset](https://iiitaphyd-my.sharepoint.com/personal/aditya_hari_research_iiit_ac_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Faditya%5Fhari%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2Fire%5Fstuff%2Fminiproject%2Fcodemixed%2Exml%2Ebz2&parent=%2Fpersonal%2Faditya%5Fhari%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2Fire%5Fstuff%2Fminiproject&ga=1) 

### About Project
Built Search Engine Platform by creating Inverted Index on the Wikipedia Data Dump (2022) of size 90 GB.

Following Steps Follows to create Inverted Indexing
* Parsing using SAX : Need to parse each page , title tag, infobox, body , category, external links and references
* Tokenization  : Tokenize sentense to get each token using regular expression using nltk for English and own tokenizer for Hindi
* Case Folding : make it all to lowercase
* Stop Words Removal : remove stop word which are more frequently occured in a sentences
* Stemming : get root/base word and store it
* Inverted Index Creation : create word & its positing list consist of doc_id : TF-IDf score
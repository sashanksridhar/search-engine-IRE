# Wikipedia Search Engine

### Required Python Libraries :
* ```xml.sax```
* ```nltk```
* ```Stemmer```

### Datasets

[Download Sample Dataset](https://drive.google.com/file/d/1tknEB9yt2AXNKJp3UvJoNRyfiTh-Nzpr/view) 

[Download 90 GB Dataset](https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/20220820/enwiki-20220820-pages-articles-multistream.xml.bz2) 

[Download Code Mix Dataset](https://iiitaphyd-my.sharepoint.com/personal/aditya_hari_research_iiit_ac_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Faditya%5Fhari%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2Fire%5Fstuff%2Fminiproject%2Fcodemixed%2Exml%2Ebz2&parent=%2Fpersonal%2Faditya%5Fhari%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2Fire%5Fstuff%2Fminiproject&ga=1) 

### About Project
Built Search Engine Platform by creating Inverted Index on the Wikipedia Data Dump (2022) of size 90 GB.

In this project two types of queries are handled : 

* Simple Queries : Ex. - ```Mahatma Gandhi```
* Multi-field queries : Ex - ```b:Mahatma i:xyz ```

The search results are ordered in ranking using a weighted TF-IDF ranking based on occurance of word in Title, Body, InfoBox and so on... 

### How to run : 


* Index Creation :

* * For English Indexer
 ``` python3 indexer.py <wikipedia_dump_path> <index_path> <stats file path>```

 * * For Hindi Indexer
  ``` python3 indexer.py <wikipedia_dump_path> <index_path> <stats file path> 1```
* Search : 
* * For English Search 
``` python3 search_index.py <index_path> <queries txt file>```
* * For Hindi Search 
``` python3 search_index.py <index_path> <queries txt file> 1```

### Implementation Details : 
* The main challenge to create an Inverted Index for a huge file has a tradeoff between the size of Inverted Index and the search time. Created 3 levels of offset files to make sure the index file loaded in the main memory at a time does not exceed space available.

Following Steps Follows to create Inverted Indexing : 

* Parsing using ```xml.sax``` parser : Need to parse each page , title tag, infobox, body , category etc...
* Tokenization : Tokenize the doc to get each token using regular expression
* Casefolding : Same case words.
* Stop Words Removal : remove stop word which are more frequently occured in a sentences ```nltk.tokenize.wordpunct_tokenize```
* Stemming : get root/base word and store it ```stemmer```
* A documentId to Title list is created at first for easy retrival of results.
* Inverted Index Creation : create words to  Positing list : 
	*  ``` DocumentID : Title Frequency : Body Frequency : infobox frequency : category frequency ```

After performing the above operations we create Intermediate Index files like 0.txt,1.txt,2.txt,... and so on. Once we are done with creating this intermediate file we perform a K-way merge to merge all these intermediate files into a single Index file. Each entry in the big Index file is a word along with its posting list. For quick retrieval of the Title's corresponding to a query have created a Document ID - Title Mapping which can be loaded into the memory while performing the Search operation.


import xml.sax
import pageProcessor
import writer
from copy import deepcopy
import os
import time

class DocParser(xml.sax.ContentHandler):

    def __init__(self, index_dir, hindi_indexer):
        self.title = ""
        self.text = ""
        self.docid = ""

        self.page_count = 0
        self.file_count = 0
        self.first = 0

        self.inverted_index = dict()

        self.istitle = False
        self.istext = False
        self.isid = False

        self.first = 0

        self.page_processor = pageProcessor.PageProcessor(hindi_indexer)
        self.writer = writer.Writer(hindi_indexer)
        self.index_dir = index_dir

        self.total_toks = 0
        self.index_toks = 0
        self.st1 = time.time()

    def startElement(self, name,attribute):
        if name == "title":
            self.istitle = True
            self.title = ""
        elif name == "text":
            self.istext = True
            self.text = ""
        elif name == "page":
            self.docid = ""
        elif name == "id":
            self.isid = True


    def characters(self, content):
        if self.istitle:
            self.title = self.title + content
        elif self.istext:
            self.text = self.text + content
        elif self.isid:
            self.docid = self.docid + content

    def endElement(self, name):

        if name == "title":
            self.istitle = False
        elif name == "text":
            self.istext = False
        elif name == "id":
            self.isid = False

        if name == "page":
            self.page_count+=1
            file_pointer = open(os.path.join(self.index_dir, "DocID_Title_mapping.txt"), 'a+', encoding='utf-8')
            if self.first == 1:
                file_pointer.write('\n')

            if self.first == 0:
                self.first = 1

            value = str(self.page_count) + ' ' + self.title
            value = value.encode('utf-8').decode('utf-8')

            file_pointer.write(value)
            file_pointer.close()

            text = deepcopy(self.text)
            title = deepcopy(self.title)

            title_frequency, total_toks, index_toks = self.page_processor.title_processing(title)

            self.total_toks += total_toks
            self.index_toks += index_toks

            text_frequency, total_toks, index_toks = self.page_processor.text_processing(text)

            self.total_toks+=total_toks
            self.index_toks+=index_toks

            for word_title in title_frequency:

                if word_title in text_frequency:
                    text_frequency[word_title]['t'] += title_frequency[word_title]
                else:
                    text_frequency[word_title] = dict(d=self.page_count, t=title_frequency[word_title], b=0, i=0, c=0, l=0,
                                            r=0)

            for term in text_frequency:
                if len(term) < 3 or term.startswith('0'):
                    continue
                text_frequency[term]['d'] = str(self.page_count)
                if term not in self.inverted_index:
                    self.inverted_index[term] = list()
                self.inverted_index[term].append(''.join(
                    tag + str(text_frequency[term][tag]) for tag in text_frequency[term] if
                    text_frequency[term][tag] != 0))


            if self.page_count % 30000 == 0:

                end = time.time()
                print("Time taken to process ",str(self.page_count), "docs ", str(end - self.st1))
                self.writer.writing_to_file(self.inverted_index, self.file_count, os.path.join(self.index_dir, 'intermediate'))
                self.file_count = self.file_count + 1
                self.inverted_index = dict()

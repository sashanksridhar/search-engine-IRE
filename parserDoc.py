import xml.sax
import pageProcessor
import writer
from copy import deepcopy
import os
import time
from collections import defaultdict

class DocParser(xml.sax.ContentHandler):

    def __init__(self, index_dir):
        self.title = ""
        self.text = ""
        self.docid = ""

        self.page_count = 0
        self.file_count = 0
        self.first = 0

        self.inverted_index = defaultdict(str)

        self.istitle = False
        self.istext = False
        self.isid = False

        self.first = 0

        self.page_processor = pageProcessor.PageProcessor()
        self.writer = writer.Writer()
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
            value = value.encode('utf-8').decode()

            file_pointer.write(value)
            file_pointer.close()

            text = deepcopy(self.text)
            title = deepcopy(self.title)

            title_frequency, total_toks, index_toks = self.page_processor.title_processing(title)

            self.total_toks += total_toks
            self.index_toks += index_toks

            words_set, body_dict, category_dict, infobox_dict, link_dict, total_toks, index_toks = self.page_processor.text_processing(text)

            self.total_toks+=total_toks
            self.index_toks+=index_toks

            for word_title in title_frequency:
                words_set.update(word_title)

            for term in words_set:
                if len(term) < 3 or term.startswith('0'):
                    continue

                posting = str(self.page_count) + ':'

                if title_frequency[term]:
                    posting += 't' + str(title_frequency[term])

                if body_dict[term]:
                    posting += 'b' + str(body_dict[term])

                if category_dict[term]:
                    posting += 'c' + str(category_dict[term])

                if infobox_dict[term]:
                    posting += 'i' + str(infobox_dict[term])

                if link_dict[term]:
                    posting += 'l' + str(link_dict[term])


                posting += ';'

                self.inverted_index[term]+=posting


            if self.page_count % 30000 == 0:
                e1 = time.time()
                print("Time for proc 30000 ", e1-self.st1)
                self.writer.writing_to_file(self.inverted_index, self.file_count, os.path.join(self.index_dir, 'intermediate'))
                self.file_count = self.file_count + 1
                self.inverted_index = defaultdict(str)

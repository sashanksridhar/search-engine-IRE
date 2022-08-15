import xml.sax
import pageProcessor
import indexer

class DocParser(xml.sax.ContentHandler):

    def __init__(self, index_dir):
        self.title = ""
        self.page_id = ""
        self.tag = ""
        self.page_flag = False
        self.text = ""
        self.page_count = 0
        self.page_id_title = ""
        self.documents_scanned = 0
        self.indexer = indexer.Indexer(index_dir)
        self.indexfile_no = 1
        self.complete_index = {"T": {}, "B": {}, "C": {}, "R": {}, "E": {}, "I": {}}

    def startElement(self, tag, attrs):
        self.tag = tag

    def characters(self, text):
        if self.tag == "id":
            if self.page_flag is False:
                self.page_id = text
                self.page_flag = True
        elif self.tag == "title":
            if self.title == "" and self.title != text:
                self.title = text
        elif self.tag == "text":
            self.text += text

    def endElement(self, tag):
        if tag == "page":
            self.page_count+=1
            d = pageProcessor.PageProcessor(self.page_id, self.title, self.text, self.complete_index)
            self.complete_index = d.get_index()

            self.page_id_title += str(self.page_id) + "," + self.title + "\n"
            self.tag = ""
            self.title = ""
            self.text = ""
            self.page_flag = False
            self.documents_scanned += 1
            if self.documents_scanned == 1000:
                self.indexfile_no, self.complete_index = self.indexer.dump_index(self.indexfile_no, self.complete_index)
                self.documents_scanned = 0

import xml.sax
import pageProcessor
import indexer
import writing

class DocParser(xml.sax.ContentHandler):

    def __init__(self, index_path):
        self.title = ""
        self.page = ""
        self.tag = ""
        self.page_count = 0
        self.writer = writing.Writing(index_path)
        self.indexing = indexer.Indexer(self.writer)

    def startElement(self, tag, attrs):
        self.tag = tag
        if tag == "page":
            self.page_count += 1


    def characters(self, text):
        if self.tag == "title":
            self.title += text
        elif self.tag == "text":
            self.page += text

    def endElement(self, tag):
        if tag == "page":
            self.writer.write_title(self.title)
            title = pageProcessor.process(self.title)

            data = self.page.lower()  # Case Folding
            data = data.split('==references==')
            if len(data) == 1:
                data = data[0].split('== references == ')
            if len(data) == 1:
                references = []
                links = []
                categories = []
            else:
                references = pageProcessor.process_references(data[1])
                links = pageProcessor.process_links(data[1])
                categories = pageProcessor.process_category(data[1])

            infobox = pageProcessor.process_infobox(data[0])
            body = pageProcessor.process_body(data[0])

            self.tag = ""
            self.title = ""
            self.text = ""

            self.indexing.index(self.page_count, title, body, categories, infobox, links, references)



import xml.sax


class DocParser(xml.sax.ContentHandler):

    def __init__(self):
        self.title = ""
        self.page = ""
        self.tag = ""

    def startElement(self, tag, attrs):
        self.tag = tag

    def characters(self, text):
        if self.tag == "title":
            self.title += text
        elif self.tag == "text":
            self.page = text

    def endElement(self, tag):
        if tag == "page":
            pass

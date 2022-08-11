import xml.sax
import pageProcessor

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
            self.page += text

    def endElement(self, tag):
        if tag == "page":
            title = pageProcessor.process(self.title)

            data = self.page.lower()  # Case Folding
            data = data.split('==references==')
            if len(data) == 1:
                data = data.split('== references == ')
            if len(data) == 1:
                references = []
                links = []
                categories = []
            else:
                references = pageProcessor.process_references(data[1])
                print(data[1])
                links = pageProcessor.process_links(data[1])
                categories = pageProcessor.process_category(data[1])

            infobox = pageProcessor.process_infobox(data[0])
            body = pageProcessor.process_body(data[0])

            print(title)
            print(references)
            print(links)
            print(categories)
            print(infobox)
            print(body)

            self.tag = ""
            self.title = ""
            self.text = ""
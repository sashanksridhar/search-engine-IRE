import xml.sax
import parserDoc

parse = xml.sax.make_parser()
parse.setFeature(xml.sax.handler.feature_namespaces, 0)
handler = parserDoc.DocParser()
parse.setContentHandler(handler)
parse.parse('sample.xml')
import xml.sax
import parserDoc
import time
index_path = "E:\\IIIT-Hyderabad\\Monsoon2022\\IRE\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602\\index_path"
parse = xml.sax.make_parser()
parse.setFeature(xml.sax.handler.feature_namespaces, 0)
handler = parserDoc.DocParser(index_path)
parse.setContentHandler(handler)
parse
start = time.time()
parse.parse('E:\\IIIT-Hyderabad\\Monsoon2022\\IRE\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602')
handler.indexing.complete(handler.page_count)
end = time.time()

print("Time taken - " + str(end - start) + " s")
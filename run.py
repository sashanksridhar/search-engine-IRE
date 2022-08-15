import xml.sax
import parserDoc
import time
from string import printable
import os
index_path = "E:\\IIIT-Hyderabad\\Monsoon2022\\IRE\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602\\index_path"
# index_path = "index_path"
parse = xml.sax.make_parser()
parse.setFeature(xml.sax.handler.feature_namespaces, 0)
handler = parserDoc.DocParser(index_path)
parse.setContentHandler(handler)
start = time.time()
parse.parse('E:\\IIIT-Hyderabad\\Monsoon2022\\IRE\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602')
# parse.parse('sample.xml')

if handler.documents_scanned > 0:
        handler.indexer.dump_index(handler.indexfile_no, handler.complete_index)

os.makedirs(os.path.dirname(index_path + "/" +"sorted/N"), exist_ok=True)

f = open(index_path + "/" +"sorted/N", "w", encoding="utf-8")
f.write(str(handler.page_count))
f.close()

pageid_to_title = filter(lambda x: x in printable, handler.page_id_title)
os.makedirs(os.path.dirname(index_path + "/" +"sorted/pagetitle"), exist_ok=True)
f = open(index_path + "/" +"sorted/pagetitle", "w", encoding="utf-8")
for title in pageid_to_title:
    f.write(title)
f.close()
end = time.time()

print("Time taken - " + str(end - start) + " s")
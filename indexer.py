import xml.sax
import parserDoc
import time
import shutil
import os
import sys
import errno

if __name__ == "__main__":
    # sys.setrecursionlimit(1500)

    # wiki_path = 'sample.xml'
    wiki_path = sys.argv[1]
    print(wiki_path)
    # wiki_path = 'E:\\IIIT-Hyderabad\\Monsoon2022\\IRE\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602'

    # index_path = "E:\\IIIT-Hyderabad\\Monsoon2022\\IRE\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602\\index_path_new"
    # index_path = "index_path"
    index_path = sys.argv[2]

    # stats_file = 'index_path/invertedindex_stat.txt'
    stats_file = sys.argv[3]
    # stats_file = "E:\\IIIT-Hyderabad\\Monsoon2022\\IRE\\enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602\\index_path_new\\invertedindex_stat.txt"

    if len(sys.argv) == 5:
        hindi_indexer = True
    else:
        hindi_indexer = False

    print(hindi_indexer)

    if not os.path.exists(os.path.join(index_path, 'intermediate')):
        try:
            os.makedirs(os.path.join(index_path, 'intermediate'))
        except OSError as e:
            if e.errno == errno.EEXIST:
                raise

    try:
        os.remove(os.path.join(index_path, 'DocID_Title_mapping.txt'))
    except OSError as e:
        pass

    try:
        os.remove(stats_file)
    except OSError as e:
        pass

    parse = xml.sax.make_parser()

    # parse.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler = parserDoc.DocParser(index_path, hindi_indexer)
    parse.setContentHandler(handler)
    start = time.time()

    parse.parse(wiki_path)

    # with open(wiki_path, "rb") as f:
    #     input_source = xml.sax.xmlreader.InputSource()
    #     input_source.setByteStream(f)
    #     input_source.setEncoding('cp1252')
    #     parse.parse(input_source)

    if handler.page_count % 30000 > 0:
        handler.writer.writing_to_file(handler.inverted_index, handler.file_count, os.path.join(index_path, 'intermediate'))
        handler.file_count += 1

    end = time.time()

    handler.writer.merge_files(handler.file_count, index_path)

    # shutil.rmtree(os.path.join(index_path,'intermediate'))
    handler.writer.create_offset_files(index_path)

    with open(stats_file, 'wb+') as stats_file:
        stats_file.write(str(handler.total_toks).encode('utf-8'))
        stats_file.write('\n'.encode('utf-8'))
        stats_file.write(str(handler.index_toks).encode('utf-8'))

    stats_file.close()


    os.remove(os.path.join(index_path, "offset_file.txt"))

    print("Time taken - " + str(end - start) + " s")


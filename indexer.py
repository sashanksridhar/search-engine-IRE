import xml.sax
import parserDoc
import time
import shutil
import os
import sys
import errno
from tqdm import tqdm

if __name__ == "__main__":
    sys.setrecursionlimit(1500)

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

    handler = parserDoc.DocParser(index_path)
    parse.setContentHandler(handler)
    start = time.time()

    parse.parse(wiki_path)

    if handler.page_count % 30000 > 0:
        handler.writer.writing_to_file(handler.inverted_index, handler.file_count, os.path.join(index_path, 'intermediate'))
        handler.file_count += 1

    end = time.time()

    handler.writer.merge_files(handler.file_count, index_path)

    shutil.rmtree(os.path.join(index_path,'intermediate'))

    with open(stats_file, 'w+', encoding='utf-8') as stats_file:
        stats_file.write(str(handler.total_toks))
        stats_file.write('\n')
        stats_file.write(str(handler.index_toks))

    stats_file.close()

    num_tokens_final = 0
    with open(os.path.join(index_path,'tokens_info.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            num_tokens_final += 1

    with open(os.path.join(index_path,'num_tokens.txt'), 'w', encoding='utf-8') as f:
        f.write(str(num_tokens_final))

    char_list = [chr(i) for i in range(97, 123)]
    num_list = [str(i) for i in range(0, 10)]

    with open(os.path.join(index_path,'tokens_info.txt'), 'r', encoding='utf-8') as f:
        for line in tqdm(f):
            if line[0] in char_list:
                with open(os.path.join(index_path, 'tokens_info_'+str(line[0])+'.txt'), 'a', encoding='utf-8') as t:
                    t.write(line.strip())
                    t.write('\n')

            elif line[0] in num_list:
                with open(os.path.join(index_path,'tokens_info_'+str(line[0])+'.txt'), 'a', encoding='utf-8') as t:
                    t.write(line.strip())
                    t.write('\n')

            else:
                with open(os.path.join(index_path, 'tokens_info_others.txt'), 'a', encoding='utf-8') as t:
                    t.write(line.strip())
                    t.write('\n')

    for ch in tqdm(char_list):
        tok_count = 0
        try:
            with open(os.path.join(index_path, f'tokens_info_{ch}.txt'), 'r', encoding='utf-8') as f:
                for line in f:
                    tok_count += 1
        except:
            print("File ", f'tokens_info_{ch}.txt', ' not found')


        with open(os.path.join(index_path, f'tokens_info_{ch}_count.txt'), 'w', encoding='utf-8') as f:
            f.write(str(tok_count))

    for num in tqdm(num_list):
        tok_count = 0
        try:
            with open(os.path.join(index_path, f'tokens_info_{num}.txt'), 'r', encoding='utf-8') as f:
                for line in f:
                    tok_count += 1
        except:
            print("File ", f'tokens_info_{num}.txt', ' not found')

        with open(os.path.join(index_path, f'tokens_info_{num}_count.txt'), 'w', encoding='utf-8') as f:
            f.write(str(tok_count))

    try:
        tok_count = 0
        with open(os.path.join(index_path, 'tokens_info_others.txt'), 'r', encoding='utf-8') as f:
            tok_count += 1

        with open(os.path.join(index_path, 'tokens_info_others_count.txt'), 'w', encoding='utf-8') as f:
            f.write(str(tok_count))
    except:
        pass

    os.remove(os.path.join(index_path,'tokens_info.txt'))


    print("Time taken - " + str(end - start) + " s")


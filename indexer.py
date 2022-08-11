from collections import defaultdict
import pickle
from writing import Writing
import heap

class Indexer():

    def __init__(self, writer:Writing):
        self.title_index = defaultdict(list)
        self.text_index = defaultdict(list)
        self.category_index = defaultdict(list)
        self.infobox_index = defaultdict(list)
        self.reference_index = defaultdict(list)
        self.links_index = defaultdict(list)
        self.writer = writer
        self.pages_per_file = 40000

    def index(self, page_count, title, body, category, infobox, link, reference):
        index = str(page_count)  # get document ID ==> Wiki page number

        category_words = dict()
        infobox_words = dict()
        text_tag_words = dict()
        title_tag_words = dict()
        reference_words = dict()
        link_words = dict()

        for i in category:
            if i not in category_words.keys():
                category_words[i] = 1
            else:
                category_words[i] += 1

        for i in infobox:
            if i not in infobox_words.keys():
                infobox_words[i] = 1
            else:
                infobox_words[i] += 1

        for i in body:
            if i not in text_tag_words.keys():
                text_tag_words[i] = 1
            else:
                text_tag_words[i] += 1

        for i in title:
            if i not in title_tag_words.keys():
                title_tag_words[i] = 1
            else:
                title_tag_words[i] += 1

        for i in reference:
            if i not in reference_words.keys():
                reference_words[i] = 1
            else:
                reference_words[i] += 1

        for i in link:
            if i not in link_words.keys():
                link_words[i] = 1
            else:
                link_words[i] += 1

        for word in text_tag_words:
            s = index + ":" + str(text_tag_words[word]);
            self.text_index[word].append(s)

        for word in title_tag_words:
            s = index + ":" + str(title_tag_words[word])
            self.title_index[word].append(s)

        for word in category_words:
            s = index + ":" + str(category_words[word])
            self.category_index[word].append(s)

        for word in infobox_words:
            s = index + ":" + str(infobox_words[word])
            self.infobox_index[word].append(s)

        for word in link_words:
            s = index + ":" + str(link_words[word])
            self.links_index[word].append(s)

        for word in reference_words:
            s = index + ":" + str(reference_words[word])
            self.reference_index[word].append(s)

        if page_count%100 == 0:
            print(page_count)

        if page_count % self.pages_per_file == 0:
            self.writer.write(self.title_index, self.text_index, self.category_index, self.infobox_index, self.reference_index, self.links_index)
            self.title_index.clear()
            self.text_index.clear()
            self.category_index.clear()
            self.infobox_index.clear()
            self.reference_index.clear()
            self.links_index.clear()

    def complete(self, page_count):
        self.writer.write(self.title_index, self.text_index, self.category_index, self.infobox_index,
                          self.reference_index, self.links_index)
        self.title_index.clear()
        self.text_index.clear()
        self.category_index.clear()
        self.infobox_index.clear()
        self.reference_index.clear()
        self.links_index.clear()

        t_file = self.writer.index_path + "/title_positions.pickle"
        file = open(t_file, "wb+")
        pickle.dump(self.writer.title_position, file)
        file.close()

        heaping = heap.Heap()
        heaping.create_heap(self.writer.index_path, self.writer.file_count, page_count)





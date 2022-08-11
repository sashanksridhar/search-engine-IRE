class Writing():
    def __init__(self, index_path):
        self.index_path = index_path
        self.title_tags = open(index_path+"/title_tags.txt", "w+", encoding="utf-8")
        self.output_files = list()
        self.title_position = list()
        self.word_position = dict()
        self.file_count = 0

    def write_title(self, title_string):
        self.title_position.append(self.title_tags.tell())

        self.title_tags.write(title_string + "\n")

    def write(self, title_index, text_index, category_index, infobox_index, reference_index, links_index):

            file = self.index_path + "/t" + str(self.file_count) + ".txt"
            outfile = open(file, "w+", encoding="utf-8")

            for word in sorted(title_index):
                posting_list = ",".join(title_index[word])
                index = word + "-" + posting_list
                outfile.write(index + "\n")
            outfile.close()

            file = self.index_path + "/b" + str(self.file_count) + ".txt"
            outfile = open(file, "w+", encoding="utf-8")
            for word in sorted(text_index):
                posting_list = ",".join(text_index[word])
                index = word + "-" + posting_list
                outfile.write(index + "\n")
            outfile.close()

            file = self.index_path + "/c" + str(self.file_count) + ".txt"
            outfile = open(file, "w+", encoding="utf-8")
            for word in sorted(category_index):
                posting_list = ",".join(category_index[word])
                index = word + "-" + posting_list
                outfile.write(index + "\n")
            outfile.close()

            file = self.index_path + "/i" + str(self.file_count) + ".txt"
            outfile = open(file, "w+", encoding="utf-8")
            for word in sorted(infobox_index):
                posting_list = ",".join(infobox_index[word])
                index = word + "-" + posting_list
                outfile.write(index + "\n")
            outfile.close()

            file = self.index_path + "/r" + str(self.file_count) + ".txt"
            outfile = open(file, "w+", encoding="utf-8")
            for word in sorted(reference_index):
                posting_list = ",".join(reference_index[word])
                index = word + "-" + posting_list
                outfile.write(index + "\n")
            outfile.close()

            file = self.index_path + "/l" + str(self.file_count) + ".txt"
            outfile = open(file, "w+", encoding="utf-8")
            for word in sorted(links_index):
                posting_list = ",".join(links_index[word])
                index = word + "-" + posting_list
                outfile.write(index + "\n")
            outfile.close()

            self.file_count += 1
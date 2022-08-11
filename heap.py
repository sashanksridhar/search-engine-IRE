from heapq import *
import os
import operator
import pickle
import math
class Heap():
    def create_heap(self, index_path, file_count, page_count):
        field_chars = ["t", "b", "i", "c", "r", "l"]
        output_files = list()
        word_position = dict()
        for f in field_chars:
            heap = []

            input_files = []
            file = index_path + "/" + f + ".txt"
            fp = open(file, "w+", encoding="utf-8")
            output_files.append(fp)
            outfile_index = len(output_files) - 1

            for i in range(file_count):
                file = index_path + "/" + f + str(i) + ".txt"
                if os.stat(file).st_size == 0:
                    try:
                        del input_files[i]
                        os.remove(file)
                    except:
                        pass
                else:
                    fp = open(file, "r", encoding="utf-8")
                    input_files.append(fp)

            if len(input_files) == 0:
                break

            # print(len(input_files))
            for i in range(file_count):
                try:
                    s = input_files[i].readline()[:-1]
                    heap.append((s, i))

                except:
                    pass

            i = 0
            heapify(heap)
            try:
                while i < file_count:
                    s, index = heappop(heap)
                    word = s[: s.find("-")]
                    posting_list = s[s.find("-") + 1:]

                    next_line = input_files[index].readline()[: -1]
                    if next_line:
                        heappush(heap, (next_line, index))
                    else:
                        i = i + 1  # one files ends here

                    if i == file_count:
                        break

                    while i < file_count:
                        next_s, next_index = heappop(heap)
                        next_word = next_s[: next_s.find("-")]
                        next_posting_list = next_s[next_s.find("-") + 1:]
                        if next_word == word:
                            posting_list = posting_list + "," + next_posting_list
                            next_new_line = input_files[next_index].readline()
                            if next_new_line:
                                heappush(heap, (next_new_line, next_index))
                            else:  # one files ends here
                                i = i + 1
                        else:
                            heappush(heap, (next_s, next_index))
                            break

                    if word not in word_position:
                        word_position[word] = dict()
                    word_position[word][f] = output_files[outfile_index].tell()
                    postings = posting_list.split(",")
                    documents = dict()
                    idf = math.log10(page_count / len(postings))
                    for posting in postings:
                        doc_id = posting[: posting.find(":")]
                        freq = int(posting[posting.find(":") + 1:])
                        tf = 1 + math.log10(freq)
                        documents[str(doc_id)] = round(tf * idf, 2)

                    documents = sorted(documents.items(), key=operator.itemgetter(1), reverse=True)

                    top_posting_list_result = ""
                    #             number_of_results = 1
                    for document in documents:
                        top_posting_list_result = top_posting_list_result + document[0] + ":" + str(document[1]) + ","
                    #                 number_of_results = number_of_results + 1
                    #                 if number_of_results > 10 :
                    #                     break

                    top_posting_list_result = top_posting_list_result[: -1]  # to remove last extra comma ","
                    output_files[outfile_index].write(top_posting_list_result + "\n")

            except IndexError:
                pass
            output_files[outfile_index].close()

            try:
                for i in range(file_count):
                    file = index_path + "/" + f + str(i) + ".txt"
                    input_files[i].close()
                    os.remove(file)
            except:
                pass
            # print(word_position)
            file = open(index_path + "/word_positions.pickle", "wb+", encoding="utf-8")
            pickle.dump(word_position, file)
            file.close()



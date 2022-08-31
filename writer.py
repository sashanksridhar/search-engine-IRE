import errno
import os
import heapq
import shutil
class Writer():

    # Writing to intermediate index
    # Example : abstent i4c1d1
    def writing_to_file(self, Inverted_Index, File_count, file_path):

        path_to_write = os.path.join(file_path, str(File_count) + '.txt')
        print(path_to_write)

        value = list()
        file_pointer = open(path_to_write, 'w+', encoding='utf-8')
        for term in sorted(Inverted_Index):
            temp = term + ' '
            temp = temp + '|'.join(item for item in Inverted_Index[term])
            value.append(temp)
        if len(value):
            file_pointer.write('\n'.join(value).encode('utf-8').decode())

        file_pointer.close()

    # Merge intermediate index files into single file
    def merge_files(self, file_count, index_path):

        if not os.path.exists(index_path):
            try:
                os.makedirs(index_path)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    raise

        file_pointer = list()
        end_of_file = list()
        list_of_words = list()
        heap = list()

        for index in range(file_count):
            path_of_file = os.path.join(index_path, 'intermediate', str(index) + '.txt')
            file_pointer.append(open(path_of_file, 'r', encoding='utf-8'))
            list_of_words.append(file_pointer[index].readline().split(' ', 1))
            if list_of_words[index][0] not in heap:
                heapq.heappush(heap, list_of_words[index][0])
            end_of_file.append(0)

        index_file_path = os.path.join(index_path, 'index_file' + '.txt')
        offset_file_path = os.path.join(index_path, "offset_file.txt")
        try:
            os.remove(index_file_path)
            os.remove(offset_file_path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        offset = 0
        flag = 0
        words = list()
        inverted_index = dict()
        while heap:
            top_most_word = heapq.heappop(heap)
            if top_most_word == "":
                continue
            words.append(top_most_word)
            if top_most_word not in inverted_index:
                inverted_index[top_most_word] = list()

            for index in range(file_count):

                if end_of_file[index] == 1:
                    continue

                if list_of_words[index][0] == top_most_word:
                    inverted_index[top_most_word].append(list_of_words[index][1].strip())
                    list_of_words[index] = file_pointer[index].readline().split(' ', 1)

                    if list_of_words[index][0] == "":
                        file_pointer[index].close()
                        end_of_file[index] = 1
                        continue

                    if list_of_words[index][0] not in heap:
                        heapq.heappush(heap, list_of_words[index][0])

            if len(words) % 100000 == 0:
                offset = self.main_file_write(words, inverted_index, index_file_path, offset_file_path, offset)
                flag = 1
                inverted_index = dict()
                words = list()

        if len(words):
            offset = self.main_file_write(words, inverted_index, index_file_path, offset_file_path, offset)

    def main_file_write(self, words, inverted_index, index_file_path, offset_file_path, offset):
        items_to_write = list()
        offset_list = list()
        try:
            file_pointer = open(index_file_path, 'a+', encoding='utf-8')
            file_pointer1 = open(offset_file_path, 'a+', encoding='utf-8')
            for word in words:
                offset_term = word + ' ' + str(offset)
                word_text = word + ' '
                word_text = word_text + '|'.join(list(item for item in inverted_index[word]))
                offset_list.append(offset_term)
                items_to_write.append(word_text)
                offset = offset + len(word_text) + 2
                # print(offset)
                # print(offset_term)

            if len(offset_list):
                file_pointer1.write('\n'.join(offset_list).encode('utf-8').decode())
                file_pointer1.write('\n')

            if len(items_to_write):
                file_pointer.write('\n'.join(items_to_write).encode('utf-8').decode())
                file_pointer.write('\n')

            file_pointer.close()
            file_pointer1.close()
        except Exception as e:
            print("Error while opening the Index File. Exiting..")
        finally:
            file_pointer.close()
            file_pointer1.close()

        return offset

    def create_offset_files(self, index_path):
        offset_path = os.path.join(index_path, 'temp_offsets')
        if not os.path.exists(offset_path):
            os.mkdir(offset_path)
        else:
            shutil.rmtree(offset_path)
            os.mkdir(offset_path)

        file_ptr = None
        with open(os.path.join(index_path, 'offset_file.txt'), encoding='utf-8') as offset_file:
            for lineno, line in enumerate(offset_file):
                if lineno % 1000000 == 0:
                    if file_ptr:
                        file_ptr = None
                    value = line.strip().split(' ')[0]
                    file_path = os.path.join(index_path, 'temp_offsets', value + '.txt')
                    file_ptr = open(file_path, "w", encoding='utf-8')
                file_ptr.write(line)
            if file_ptr:
                file_ptr.close()




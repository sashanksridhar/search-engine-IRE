import errno
import os
import heapq
import shutil
from tqdm import tqdm
from collections import defaultdict
import re
class Writer():
    def writing_to_file(self, Inverted_Index, File_count, file_path):

        path_to_write = os.path.join(file_path, str(File_count) + '.txt')
        print(path_to_write)
        # print("File",str(File_count))
        file_pointer = open(path_to_write, 'w+', encoding='utf-8')
        temp_index_map = sorted(Inverted_Index.items(), key=lambda item: item[0])
        temp_index = []
        for word, posting in tqdm(temp_index_map):
            temp_index.append(word + '-' + posting)

        if len(temp_index):
            file_pointer.write('\n'.join(temp_index).encode('utf-8').decode())

        file_pointer.close()

    def write_final_files(self,  data_to_merge, num_files_final, index_path):

        title_dict, body_dict, category_dict, infobox_dict, link_dict = defaultdict(dict), defaultdict(
            dict), defaultdict(dict), defaultdict(dict), defaultdict(dict)

        unique_tokens_info = {}

        sorted_data = sorted(data_to_merge.items(), key=lambda item: item[0])

        for i, (token, postings) in tqdm(enumerate(sorted_data)):
            for posting in postings.split(';')[:-1]:

                id = posting.split(':')[0]

                fields = posting.split(':')[1]

                if 't' in fields:
                    title_dict[token][id] = re.search(r'.*t([0-9]*).*', fields).group(1)

                if 'b' in fields:
                    body_dict[token][id] = re.search(r'.*b([0-9]*).*', fields).group(1)

                if 'c' in fields:
                    category_dict[token][id] = re.search(r'.*c([0-9]*).*', fields).group(1)

                if 'i' in fields:
                    infobox_dict[token][id] = re.search(r'.*i([0-9]*).*', fields).group(1)

                if 'l' in fields:
                    link_dict[token][id] = re.search(r'.*l([0-9]*).*', fields).group(1)


            token_info = '-'.join([token, str(num_files_final), str(len(postings.split(';')[:-1]))])
            unique_tokens_info[token] = token_info + '-'

        final_titles, final_body_texts, final_categories, final_infoboxes, final_links, final_references = [], [], [], [], [], []

        for i, (token, _) in tqdm(enumerate(sorted_data)):

            if token in title_dict.keys():
                posting = title_dict[token]
                final_titles = self.get_diff_postings(token, posting, final_titles)
                t = len(final_titles)
                unique_tokens_info[token] += str(t) + '-'
            else:
                unique_tokens_info[token] += '-'

            if token in body_dict.keys():
                posting = body_dict[token]
                final_body_texts = self.get_diff_postings(token, posting, final_body_texts)
                t = len(final_body_texts)
                unique_tokens_info[token] += str(t) + '-'
            else:
                unique_tokens_info[token] += '-'

            if token in category_dict.keys():
                posting = category_dict[token]
                final_categories = self.get_diff_postings(token, posting, final_categories)
                t = len(final_categories)
                unique_tokens_info[token] += str(t) + '-'
            else:
                unique_tokens_info[token] += '-'

            if token in infobox_dict.keys():
                posting = infobox_dict[token]
                final_infoboxes = self.get_diff_postings(token, posting, final_infoboxes)
                t = len(final_infoboxes)
                unique_tokens_info[token] += str(t) + '-'
            else:
                unique_tokens_info[token] += '-'

            if token in link_dict.keys():
                posting = link_dict[token]
                final_links = self.get_diff_postings(token, posting, final_links)
                t = len(final_links)
                unique_tokens_info[token] += str(t) + '-'
            else:
                unique_tokens_info[token] += '-'

        with open(os.path.join(index_path, "tokens_info.txt"), 'a', encoding='utf-8') as f:
            f.write('\n'.join(unique_tokens_info.values()))
            f.write('\n')

        self.write_diff_postings('title', final_titles, num_files_final, index_path)

        self.write_diff_postings('body', final_body_texts, num_files_final, index_path)

        self.write_diff_postings('category', final_categories, num_files_final, index_path)

        self.write_diff_postings('infobox', final_infoboxes, num_files_final, index_path)

        self.write_diff_postings('link', final_links, num_files_final, index_path)

        num_files_final += 1

        return num_files_final

    def get_diff_postings(self, token, postings, final_tag):

        postings = sorted(postings.items(), key=lambda item: int(item[0]))

        final_posting = token + '-'
        for id, freq in postings:
            final_posting += str(id) + ':' + freq + ';'

        final_tag.append(final_posting.rstrip(';'))

        return final_tag

    def write_diff_postings(self, tag_type, final_tag, num_files_final, index_path):

        with open(os.path.join(index_path, tag_type+"_data_"+str(num_files_final) + '.txt'), 'w') as f:
            f.write('\n'.join(final_tag))


    def merge_files(self, file_count, index_path):

        files_data = {}
        line = {}
        postings = {}
        is_file_empty = {i: 1 for i in range(file_count)}
        tokens = []
        i = 0
        while i < file_count:

            files_data[i] = open(os.path.join(index_path, 'intermediate', str(i) + '.txt'), 'r', encoding='utf-8')

            line[i] = files_data[i].readline().strip('\n')
            postings[i] = line[i].split('-')
            is_file_empty[i] = 0
            new_token = postings[i][0]
            if new_token not in tokens:
                tokens.append(new_token)
            i += 1

        tokens.sort(reverse=True)
        num_processed_postings = 0
        data_to_merge = defaultdict(str)
        num_files_final = 0

        while sum(is_file_empty.values()) != file_count:

            token = tokens.pop()
            num_processed_postings += 1

            if num_processed_postings % 30000 == 0:
                num_files_final = self.write_data.write_final_files(data_to_merge, num_files_final)

                data_to_merge = defaultdict(str)
            i = 0
            while i < file_count:

                if is_file_empty[i] == 0:

                    if token == postings[i][0]:

                        line[i] = files_data[i].readline().strip('\n')
                        data_to_merge[token] += postings[i][1]

                        if len(line[i]):
                            postings[i] = line[i].split('-')
                            new_token = postings[i][0]

                            if new_token not in tokens:
                                tokens.append(new_token)
                                tokens.sort(reverse=True)

                        else:
                            is_file_empty[i] = 1
                            files_data[i].close()
                            print(f'Removing file {str(i)}')
                            os.remove(os.path.join(index_path,'intermediate', str(i) + '.txt'))
                i += 1

        num_files_final = self.write_final_files(data_to_merge, num_files_final, index_path)

        return num_files_final



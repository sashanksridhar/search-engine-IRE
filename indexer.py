from typing import Dict
import gevent
import os
class Indexer():
    def __init__(self, index_dir):
        self.index_dir = index_dir

    def dump_index(self,indexfile_no, complete_index:Dict):
        self.create_index(indexfile_no, complete_index)
        complete_index = {"T": {}, "B": {}, "C": {}, "R": {}, "E": {}, "I": {}}
        indexfile_no += 1
        return indexfile_no, complete_index

    def create_index(self, indexfile_no, complete_index:Dict):
        """
            Write the complete_index to a file with a different format
        """

        # @Todo: Yet to sort by tf in each file

        threads = []
        for section in complete_index:
            threads.append(gevent.spawn(self.write_to_index, section, indexfile_no, complete_index))
        gevent.joinall(threads)

    def write_to_index(self, section,indexfile_no, complete_index:Dict):

        index_mappings = {"T": "title/",
                          "B": "body/",
                          "C": "category/",
                          "R": "references/",
                          "E": "links/",
                          "I": "infobox/"}

        category_index = complete_index

        filename = self.index_dir + "/" + index_mappings[section] + "file" + str(indexfile_no)
        # Store current sys.stdout
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # prev_stdout = sys.stdout
        f = open(filename, "w", encoding="utf-8")

        for token in sorted(category_index[section].items()):
            line = token[0] + "#"
            for doc_id in token[1]:
                line += hex(int(doc_id))[2:] + "-" + \
                        str(category_index[section][token[0]][doc_id]) + ";"
            f.write(line)
            # line[:-1].encode("utf-8")

        # Restore sys.stdout
        # sys.stdout = prev_stdout

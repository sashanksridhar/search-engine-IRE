import time
from search_utils import *
import sys
from query import *
import os


def get_titles(index_path):
	titles = dict()
	with open(os.path.join(index_path, 'DocID_Title_mapping.txt'), 'r', encoding='utf-8') as file_ptr:
		for line in file_ptr.readlines():
			line = line.strip().split(' ', 1)
			if len(line) == 1:
				pass
			else:
				titles[int(line[0])] = line[1]

	return titles


index_path = sys.argv[1]
query_path = sys.argv[2]
if len(sys.argv) == 4:
	hindi_query = True
else:
	hindi_query = False
print("Loading Titles-Document ID Mappings....")
titles = get_titles(index_path)
number_document = len(titles)
print("Loaded...")

# output_path = sys.argv[2]
#file_ptr_output = open(output_path, 'w+')



with open(query_path, "r", encoding='utf-8') as f:
	with open('queries_op.txt', 'w', encoding='utf-8') as w:
		while True:
			query_str = f.readline()
			if not query_str:
				break

			start = time.time()
			processed_queries = query_processing(query_str, hindi_query)
			# print(processed_queries)
			result = searching(processed_queries,index_path,number_document)
			end = time.time()
			#print(result)
			print("Results : ")
			if len(result) > 0:
				if len(result) > 10:
					result = result[:10]
				for r in result:
					print(r[0])
					print(titles[r[0]])

					w.write(str(r[0])+", "+titles[r[0]]+"\n")

					#file_ptr_output.write('\n')
			#file_ptr_output.write('\n')
			#file_ptr_output.write('\n')
			print("Response Time for the Query " + query_str + " is " + str(end - start) + " seconds")
			w.write(str(end-start)+"\n")
			w.write("\n")



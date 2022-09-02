import os
import re
import math
import operator

# Binary Search Lower Bound
def lower_bound_search(list_of_files,target):
	l,r = 0, len(list_of_files) - 1

	while l <= r:
		mid = int(l + (r - l) / 2)
		if list_of_files[mid] < target:
			l = mid + 1
		else:
			r = mid - 1

	return list_of_files[l-1]


def get_offsets(file_name, index_path):
	"""
	Returns a list containing all the offsets based on the file_name given
	"""
	file_path = os.path.join(os.path.join(index_path, 'temp_offsets'),file_name)
	with open(file_path,'r', encoding='utf-8') as file_ptr:
		offset = [int(line.strip().split(' ')[1]) for line in file_ptr.readlines()]
	return offset

# Binary search a word
def get_offset(word,low,high,file_ptr,list_offsets):

	while low <= high:
		mid = (high + low)/2
		# print(list_offsets[int(mid)])
		file_ptr.seek(list_offsets[int(mid)])
		# print(file_ptr.readline().strip().split(' '))
		value,offset = file_ptr.readline().strip().split(' ')
		another_value,offset1 = file_ptr.readline().strip().split(' ')
		# print(word)
		# Even and Odd matches
		if value == word:
			return list_offsets[int(mid)]
		if another_value == word:
			return list_offsets[int(mid) + 1]
		#If not matched
		if value < word:
			low = mid + 1
		else:
			high = mid - 1
	return - 1

def get_posting_list(index_file,offset_value,key):
	index_file.seek(offset_value)
	line = index_file.readline().strip().split(' ')[1].split('|')
	# Generic Search
	if key == 'all':
		return line
	# Field Queries
	value = list(v for v in line if key in v)
	return value

# Page Rank
def ranking(pages,number_document):
	values = dict()
	for page in pages:
		for tag in pages[page]:
			if len(pages[page][tag]) == 0:
				continue
			temp = math.log(number_document/len(pages[page][tag]))
			for field_value in pages[page][tag]:
				if field_value[0] not in values:
					values[field_value[0]] = 0.0
				if tag == 't':
					values[field_value[0]] += temp *(math.log(field_value[1] + 1)) * 30
				if tag == 'b':
					values[field_value[0]] += temp *(math.log(field_value[1] + 1)) * 30
				if tag == 'c':
					values[field_value[0]] += temp *(math.log(field_value[1] + 1)) * 20
				if tag == 'i':
					values[field_value[0]] += temp *(math.log(field_value[1] + 1)) * 8
				if tag == 'l':
					values[field_value[0]] += temp *(math.log(field_value[1] + 1)) * 6
				if tag == 'r':
					values[field_value[0]] += temp *(math.log(field_value[1] + 1)) * 6

	result = sorted(values.items(), key= operator.itemgetter(1), reverse=True)
	return result[:10]


def searching(query,index_path,number_document):
	index_path_file = os.path.join(index_path, 'index_file.txt')
	index_file_ptr = open(index_path_file,'r', encoding='utf-8')
	result = dict()
	list_of_files = []
	for file in os.listdir(os.path.join(index_path, "temp_offsets")):
		list_of_files.append(file)

	list_of_files.sort()
	for key in query:
		if key in ['all']:
			for word in query['all']:
				file_name = lower_bound_search(list_of_files,word)

				offsets = get_offsets(file_name, index_path)
				offset = get_offset(word,0,len(offsets), index_file_ptr,offsets)
				if offset == -1:
					continue
				posting_list = get_posting_list(index_file_ptr,offset,'all')

				result[word] = {'t': list(), 'b': list(), 'i': list(), 'c': list(), 'l': list(), 'r': list()}
				for posting in posting_list:
					document_id = int(re.findall('d[0-9]+',posting)[0][1:])
					if 't' in posting:
						title_value = int(re.findall('t[0-9]+', posting)[0][1:])
						result[word]['t'].append([document_id,title_value])
					if 'b' in posting:
						body_value = int(re.findall('b[0-9]+',posting)[0][1:])
						result[word]['b'].append([document_id,body_value])
					if 'c' in posting:
						category_value = int(re.findall('c[0-9]+',posting)[0][1:])
						result[word]['c'].append([document_id,category_value])
					if 'i' in posting:
						infobox_value = int(re.findall('i[0-9]+',posting)[0][1:])
						result[word]['i'].append([document_id,infobox_value])
					if 'r' in posting:
						ref_value = int(re.findall('r[0-9]+',posting)[0][1:])
						result[word]['r'].append([document_id,ref_value])
					if 'l' in posting:
						body_value = int(re.findall('l[0-9]+',posting)[0][1:])
						result[word]['l'].append([document_id,body_value])
		else:
			for word in query[key]:
				file_name = lower_bound_search(list_of_files,word)
				offsets = get_offsets(file_name, index_path)
				offset = get_offset(word,0,len(offsets), index_file_ptr, offsets)
				if offset == -1:
					continue
				# mapping = {'title' : 't', 'body' : 'b', 'infobox': 'i', 'category': 'c', 'links':'l', 'ref' : 'r'}
				# print(key)
				# if len(key) != 1:
				# 	key1 = mapping[key]
				# else:

				key1 = key
				posting_list = get_posting_list(index_file_ptr, offset, key1)
				#print("Posting List")
				#print(posting_list)
				if word not in result:
					result[word] = dict()
				result[word][key1] = list()
				for posting in posting_list:
					document_id = int(re.findall('d[0-9]+',posting)[0][1:])
					if key1 == 't':
						t = re.compile('t[0-9]+')
						title_value = int(t.findall(posting)[0][1:])
						result[word][key1].append([document_id, title_value])
					elif key1 == 'b':
						b = re.compile('b[0-9]+')
						body_value = int(b.findall(posting)[0][1:])
						result[word][key1].append([document_id, body_value])
					elif key1 == 'c':
						c = re.compile('c[0-9]+')
						category_value = int(c.findall(posting)[0][1:])
						result[word][key1].append([document_id, category_value])
					elif key1 == 'l':
						l = re.compile('l[0-9]+')
						links_value = int(l.findall(posting)[0][1:])
						result[word][key1].append([document_id, links_value])
					elif key1 == 'i':
						i = re.compile('i[0-9]+')
						infobox_value = int(i.findall(posting)[0][1:])
						result[word][key1].append([document_id, infobox_value])
					elif key1 == 'r':
						r = re.compile('r[0-9]+')
						ref_value = int(r.findall(posting)[0][1:])
						result[word][key1].append([document_id, ref_value])

	ranked_result = ranking(result, number_document)
	return ranked_result



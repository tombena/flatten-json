import json, os, io, fcntl
from pprint import pprint
from pathlib import Path

# add JSON dictionary to a new file, edit file if necessary
# filename: name of the edited file
# dic: JSON dictionary that should be added
def write_to_file(filename, d):

	# list of dictionaries
	dicts = []

	my_file = Path(filename)

	# file doesn't exist
	if not my_file.is_file():
		f = open(filename, 'w')
		fcntl.flock(f, fcntl.LOCK_EX)

	else:

		f = open(filename, 'r+')
		fcntl.flock(f, fcntl.LOCK_EX)

		# convert content back to JSON
		data = json.load(f)

		for i in range(len(data)):
			# append all JSON blocks in correct order
			# (from oldest to most recent)
			dicts.append(data[i])

		# go back to beginning of file
		f.seek(0)

	dicts.append(d)

	json.dump(dicts, f)

	fcntl.flock(f, fcntl.LOCK_UN)

	f.close()

	return

# recursively flatten JSON block
# obj: current JSON block
# parent_name: parent name
# key: current key
# depth + 1: number of times this function was called
# j_ids: dict of JSON ids
def flatten(obj, parent_name, key, depth, j_ids):
	# print("depth = " + str(depth))
	# print("key = " + key)
	# print("parent_name = " + parent_name)

	# depth has to be smaller than 5
	if (depth > 5):
		return
	# elif (depth != 0):
	# 	key = key[:-1]

	# create dictionary
	d = {}



	# print(obj)
	# print(type(obj))

	# if type(obj) == dict and len(obj) == 1:
	# 	elem = obj

	elem = obj
	if len(obj) == 1:
		try:
			elem = obj[key][0]
		except KeyError:
			print(" ")

	# for each field in dictionary
	for key, value in elem.items():
		if type(value) == dict:
			# print(value)
			# print("len = " + str(len(value)))
			flatten(value, parent_name + "_" + key, key, depth + 1, j_ids)
		elif type(value) == list:
			# need to iterate through the list
			for i in range(len(value)):
				j_ids["_index"] = i
				# key is plural therefore the last 's' should be removed
				# (considering plural of name doesn't become "-es" e.g. baby -> babies)

				flatten(value[i], parent_name + "_" + key[:-1], key, depth + 1, j_ids)
		else:
			d[key] = value

	# print(parent_name + " of depth " + str(depth) + ":")
	# print(d)

	if len(d) == 0:
		return

	# set JSON id fields (there can be multiple of them)
	d = {**d, **j_ids}

	write_to_file('output/' + parent_name + '.json', d)

	return

# input files are in input/ folder
for file in os.listdir("input/"):
	if file.endswith("donuts.json"):
		# for every file in input/ folder
		input = open("input/" + file, 'r')

		# decode JSON from input
		data = json.load(input)

		# remove ".json" (5 char long) from filename
		parent_name = file[:-5];
		# print(parent_name)

		j_ids = {"id": data[parent_name][0]["id"]}
		# print(j_ids)

		flatten(data, parent_name[:-1], parent_name, 0, j_ids)

		input.close()

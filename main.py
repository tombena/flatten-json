import json, os, io, fcntl
from pprint import pprint
from pathlib import Path

# if there are nested lists then there could be collision
# with "_index", therefore if "_index" already exists
# prefix with another "_" etc...
def new_index(j_ids):

	curr_index = "_index"

	while (curr_index in j_ids):
		curr_index = "_" + curr_index

	return curr_index

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

	# depth has to be smaller than 5
	if (depth > 5):
		return

	# create dictionary
	d = {}

	# set JSON id fields (there can be multiple of them)
	# j_ids shouldn't be modified
	d = {**d, **j_ids}

	elem = obj
	if len(obj) == 1:
		try:
			elem = obj[key][0]
		except KeyError:
			elem = obj

	# for each field in dictionary
	for key, value in elem.items():
		if type(value) == dict:
			# print(value)
			# print("len = " + str(len(value)))
			flatten(value, parent_name + "_" + key, key, depth + 1, j_ids.copy())
		elif type(value) == list:
			# print(value)

			if len(value) == 0:
				d[key] = value
			elif type(value[0]) != dict:
				d[key] = value
			else:
				# need to iterate through the list
				for i in range(len(value)):

					if len(value) > 1:
						# need a new field (explicit copy)
						t_ids = j_ids.copy()

						curr_index = new_index(j_ids)

						# create new "_index" field if necessary (add "_")
						t_ids[curr_index] = i

						# key is plural therefore the last 's' should be removed
						# (considering plural of name doesn't become "-es" e.g. baby -> babies)

						flatten(value[i], parent_name + "_" + key[:-1], key, depth + 1, t_ids.copy())
					else:
						flatten(value[i], parent_name + "_" + key[:-1], key, depth + 1, j_ids.copy())
		else:
			d[key] = value

	if len(d) == len(j_ids):
		return

	write_to_file('output/' + parent_name + '.json', d)

	return

# input files are in input/ folder
for file in os.listdir("input/"):
	if file.endswith(".json"):
		# for every file in input/ folder
		input = open("input/" + file, 'r')

		# decode JSON from input
		data = json.load(input)

		# remove ".json" (5 char long) from filename
		parent_name = file[:-5];

		j_ids = {"id": data[parent_name][0]["id"]}

		flatten(data, parent_name[:-1], parent_name, 0, j_ids)

		input.close()

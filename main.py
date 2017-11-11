import json
from pprint import pprint

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
	elif (depth != 0):
		key = key[:-1]

	# create dictionary
	d = {}

	# set JSON id fields (there can be multiple of them)
	d = {**d, **j_ids}

	# print("depth = " + str(depth))
	# print("key = " + key)
	# print(type(obj))
	# print(obj)
	# print(len(obj))

	if len(obj) == 1:
		print("len(obj) == 1 + " + str(type(obj)))
		elem = obj[key][0]
	else:
		print("len(obj) != 1 + " + str(type(obj)))
		elem = obj

	# for each field
	for key, value in elem.items():
		if type(value) == dict:
			flatten(value, parent_name + "_" + key, key, depth + 1, j_ids)
		elif type(value) == list:
			# need to iterate through the list
			for i in range(len(value)):
				j_ids["_index"] = i
				# key is plural
				flatten(value[i], parent_name + "_" + key[:-1], key, depth + 1, j_ids)
		else:
			d[key] = value


	print(parent_name + " of depth " + str(depth) + ":")
	print(d)

	# write to output/
	output = open('output/' + parent_name + '.json', 'w')
	json.dump(d, output)
	output.close()

	return


# for every file in input/ folder
input = open('input/restaurants.json', 'r')

# decode JSON from input
data = json.load(input)

pprint(data)


# filename - ".json"
parent_name = "restaurants";

j_ids = {"id": data[parent_name][0]["id"]}
print(j_ids)

flatten(data, parent_name[:-1], parent_name, 0, j_ids)




input.close()
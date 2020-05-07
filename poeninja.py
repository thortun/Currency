import util as u
import requests
import os
from os.path import join
import json

TYPES = ["Currency",
		"Fragment",
		"Oil",
		"Incubator",
		"Scarab",
		"Fossil",
		"Resonator",
		"Essence",
		"DivinationCard",
		"Prophecy",
		"SkillGem",
		"BaseType",
		"HelmetEnchant",
		"UniqueMap",
		"UniqueJewel",
		"UniqueWeapon",
		"UniqueFlask",
		"UniqueArmour",
		"UniqueAccessory",
		"Beast",
		"DeliriumOrb",
		"Watchstone"
		]

def gen_url(league, item_type):
	payload = "?league={0}&type={1}".format(league, item_type)
	overview_type = "itemoverview"
	if item_type.lower() in ("currency", "fragment"):
		overview_type = "currencyoverview"
	return "https://poe.ninja/api/data/" + overview_type + payload

def get_name_dict():
	return u.dict_from_json_file("data/poeninja/namedict.json")

def update_database():
	"""Updates the database from poeninja."""
	league = "Delirium"

	for item_type in TYPES:
		url = gen_url(league, item_type)
		print("Downloading " + item_type)
		data = requests.get(url).text
		filename = file_path_from_type(item_type)
		with open(filename, "w", encoding="utf-8") as fileID:
			fileID.write(data)

def file_path_from_type(item_type):
	"""Gets the location of a file
	based on item_type.
	"""
	return "data/poeninja/{0}.json".format(item_type)

def update_name_dict():
	"""Updates the name dict."""
	type_ignore = ["BaseType",
					"HelmetEnchant"]

	name_dict = dict()
	for item_type in TYPES:
		if item_type not in type_ignore:
			path = file_path_from_type(item_type)
			print(path)
			item_dict = u.dict_from_json_file(path)
			for line in item_dict["lines"]:
				if "chaosValue" in line:
					name = line["name"]
					value = line["chaosValue"]
				elif "receive" in line:
					name = line["currencyTypeName"]
					value = line["receive"]["value"]
				name_dict[name] = value
	with open("data/poeninja/namedict.json", "w") as fileID:
		fileID.write(json.dumps(name_dict))

def main():
	update_database()
	update_name_dict()


if __name__ == '__main__':
	main()
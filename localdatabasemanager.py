import poeninja # update_database, update_name_dict
import requests
from poedatabase import database
from util import dict_from_json_file

def update_stats():
	"""Updates the database of stats."""
	url = "https://www.pathofexile.com/" + "api/trade/data/stats"
	save_path = "data/stats.json"
	r = requests.get(url)
	with open(save_path, "w") as fileID:
		fileID.write(r.text)

def update_items():
	url = "https://www.pathofexile.com/" + "api/trade/data/items"
	save_path = "data/items.json"
	r = requests.get(url)
	with open(save_path, "w") as fileID:
		fileID.write(r.text)

def update_mod_database():
	"""Updates the mod database."""
	mydb = database()
	cursor = mydb.cursor()
	mod_path = "data/stats.json"
	info = dict_from_json_file(mod_path)
	cursor.execute("DELETE FROM poe.mod")	# Clear table
	for mod_type in info["result"]:
		for mod in mod_type["entries"]:
			mod_id = mod["id"]
			mod_text = mod["text"]
			mod_type = mod["type"]
			# If the mod has options we need to add these to the options table
			if "option" in mod:
				query = "INSERT INTO poe.mod (id, text, type, options) VALUES (%s, %s, %s, %s);"
				val = (mod_id, mod_text, mod_type, 1)
				cursor.execute(query, val)
				for option_mod in mod["option"]["options"]:
					option_mod_id = option_mod["id"]
					option_mod_text = option_mod["text"]
					mod_query 	= "INSERT INTO poe.options (mod_id, id, text) VALUES (%s, %s, %s)"
					mod_val 	= (mod_id, option_mod_id, option_mod_text)
					cursor.execute(mod_query, mod_val)
			# If there are no mods, simply add the mod to the table
			else:
				query = "INSERT INTO poe.mod (id, text, type) VALUES (%s, %s, %s);"
				val = (mod_id, mod_text, mod_type)
				cursor.execute(query, val)
	mydb.commit()

def mod_text_to_id(mod_text):
	pass

def random_mod(mydb):
	"""Gets a random mod."""
	cursor = mydb.cursor()
	cursor.execute("SELECT * FROM poe.mod ORDER BY RAND() LIMIT 1")
	result = cursor.fetchone()
	if result[3] == 1:
		print(result)
		option_query = "SELECT * FROM poe.options WHERE mod_id='%s' ORDER BY RAND() LIMIT 1" % result[0]
		print(option_query)
		cursor.execute(option_query)
		option_result = cursor.fetchone()
		print(result[1].replace("#", str(option_result[2])))
	else:
		pass

def update():
	"""Updates all local databases."""
	#print("Updating poeninja database...")
	#poeninja.update_database()
	#print("Updateing poeninja name-dict...")
	#poeninja.update_name_dict()
	#print("Updating stats...")
	#update_stats()
	#print("Updating items...")
	#update_items()
	#print("Updating mod MySQL database...")
	#update_mod_database()
	mydb = database()
	while True:
		random_mod(mydb)


if __name__ == "__main__":
	update()
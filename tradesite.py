import requests
import json
# https://www.reddit.com/r/pathofexiledev/comments/7aiil7/how_to_make_your_own_queries_against_the_official/

def post_trade_request(payload):
	"""Gets the items from a query."""	
	url = "https://www.pathofexile.com/api/trade/search/Delirium"
	r = requests.post(url = url, json = payload)
	return r.json()

def get_filters(item):
	filters = dict()
	filters["type_filters"] = {"disabled" : False, "rarity" : {"option" : "rare"}}
	return filters

def item_to_query(item):
	"""Returns a trade-query given the item
	Finds items with the same mods.
	"""
	v = dict()
	v["price"] = "asc"
	query = dict()
	stats = []
	query["stats"] = stats
	#query["name"] = ""
	#query["type"] = ""
	v["query"] = query
	stat_filter = dict()
	stat_filter["type"] = "and"
	stat_filter["filters"] = []
	stat_filter["disabled"] = False
	stats.append(stat_filter)
	for explicit_mod in item["explicitMods"]:
		mod_id, values = mod_to_mod_id(explicit_mod)
		min_value = values[0]
		stat_filter["filters"].append({"id" : mod_id, "value" : {"min": min_value}})

	return v

def mod_to_mod_id(mod):
	"""Returns the mod-id given a string representing the mod.
	E.g. +15 strength ==> (pseudo.pseudo_total_strength, [15])
	"""
	words = mod.split(" ")
	values = []
	all_mods = json.loads(open("temp/tradeapistats.json", "r").read())
	for i, word in enumerate(words):
		L = len(word)
		if word[0] == "+" and word[-1] == "%":
			words[i] = "#%"
			values.append(word[1:L - 1])
		elif word[0] == "-" and word[-1] == "%":
			words[i] = "#%"
			values.append(word[1:L - 1])
		elif word[0] == "+":
			words[i] = "#"
			values.append(word[1:L])
		elif word[0] == "-":
			words[i] = "#"
			values.append(word[1:L])
		elif word[-1] == "%":
			words[i] = "#%"
			values.append(word[0:L - 1])
	mod_string = " ".join(words)
	for mod_type in all_mods:
		for specific_mod in mod_type["entries"]:
			if specific_mod["text"] == mod_string:
				return specific_mod["id"], values
	return "NO_ID", 0

def id_to_item(item_id, query_id = ""):
	fetch_url = "https://www.pathofexile.com/api/trade/fetch/" + item_id + "?query=" + query_id
	r = requests.get(fetch_url)
	item = r.json()
	return item

def get_price(item):
	"""Returns the price of the item."""
	currency = item["listing"]["price"]["currency"]
	amount	 = item["listing"]["price"]["amount"]
	return amount

def main():
	item = json.loads(open("rareexample.json", "r").read())
	query = item_to_query(item)
	resp = post_trade_request(query)
	first_id = resp["result"][0]
	new_item = id_to_item(first_id)["result"][0]
	print(get_price(new_item))

if __name__ == '__main__':
	main()

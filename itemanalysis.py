import util as u
import itemutil as iu
import poeninja as pn
from poeitems import get_item
from poeitems import PoEItem, FrameType 

def main():
	stash_data_path = "data/stash.json"
	stash = u.dict_from_json_file(stash_data_path)
	frame_types = set()
	item_list = []
	for tab in stash["tabs"]:
		for item_dict in tab["items"]:
			item = get_item(item_dict)
			item_list.append(item)

	i = 0
	for item in item_list:
		item.get_price()
		if item.value == -1 and item.frame_type == FrameType.Unique:
			print(item)
			print("\t{:.2g}".format(item.value))

if __name__ == '__main__':
	main()
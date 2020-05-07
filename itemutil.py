def get_stack_size_dirty(item):
	stack_size_property = find_property_by_name(item, "Stack Size")
	return int(stack_size_property["values"][0][0][0])

def find_property_by_name(item, name):
	for p in item["properties"]:
		if p["name"] == name:
			return p
	return None
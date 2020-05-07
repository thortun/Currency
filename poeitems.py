import enum
import util as u
# UNIQUE STUFF
import poeninja as pn
# RARE STUFF
import tradesite
from tradesite import mod_to_mod_id

def get_item(item_data):
	"""Returns the correct version of the item."""
	frame_type = FrameType(int(item_data["frameType"]))
	if frame_type == FrameType.Rare:
		return RareItem(item_data)
	elif frame_type == FrameType.Currency:
		return Currency(item_data)
	else:
		return PoEItem(item_data)

class FrameType(enum.Enum):
	Normal 			= 0
	Magic			= 1
	Rare 			= 2
	Unique			= 3
	Gem 			= 4
	Currency		= 5
	DivinationCard 	= 6
	Prophecy 		= 8

class ItemType(enum.Enum):
	Undecided 		= 0
	BaseType		= 1
	Beast			= 2
	Currency		= 3
	DivinationCard	= 4
	Essence			= 5
	Fossil			= 6
	Fragment		= 7
	Incubator		= 8
	Oil				= 9
	Prophecy		= 10
	Resonator		= 11
	Scarab			= 12
	SkillGem		= 13

class PoEItem:
	def __init__(self, item_data):
		self.item_data 	= item_data				# Cache item data
		self.type_line 	= item_data["typeLine"]	# Get the typeline, e.g. "Broad Sword"
		self.name 		= item_data["name"]		# Name of the item, e.g. "Killer Smoker"
		self.value = -1							# Set value to -1 at start
		self.decide_frame_type()				# Decide the frame type, i.e. rarity

	def decide_frame_type(self):
		frame_type = self.item_data["frameType"]
		if frame_type == 0:
			self.frame_type = FrameType.Normal 
		elif frame_type == 1:
			self.frame_type = FrameType.Magic 
		elif frame_type == 2:
			self.frame_type = FrameType.Rare 
		elif frame_type == 3:
			self.frame_type = FrameType.Unique 
		elif frame_type == 4:
			self.frame_type = FrameType.Gem 
		elif frame_type == 5:
			self.frame_type = FrameType.Currency 
		elif frame_type == 6:
			self.frame_type = FrameType.DivinationCard
		else:
			self.frame_type = FrameType.Normal

	def get_price(self):
		name_dict = pn.get_name_dict()
		if self.name in name_dict:
			self.value = name_dict[self.name]
		elif self.type_line in name_dict:
			self.value = name_dict[self.type_line]

	def identified(self):
		return self.item_data["identified"]

	def __str__(self):
		string = ""
		if not self.identified():
			string = "(UID) "
		string += "%s %s\n%s" % (self.name, self.type_line, self.frame_type.name)
		if "enchantMods" in self.item_data:
			for mod in self.item_data["enchantMods"]:
				string += "\n" + mod
			string += "\n"
		if "explicitMods" in self.item_data:
			for mod in self.item_data["explicitMods"]:
				string += "\n" + mod #mod_to_mod_id(mod)[0]
			string += "\n"
		return string	

	def rarity_string(self):
		col = ""
		if self.frame_type == FrameType.Rare:
			col = bcolors.WARNING
		elif self.frame_type == FrameType.Unique:
			col = bcolors.FAIL
		elif self.frame_type == FrameType.Magic:
			col = bcolor.OKBLUE
		rar_str = col + self.frame_type.name
		if col:
			rar_str += bcolors.ENDC
		return rar_str

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class RareItem(PoEItem):
	"""Rare item"""
	pass
	
class UniqueItem(PoEItem):
	"""Unique item."""
	pass

class Currency(PoEItem):
	"""Currency"""
	pass
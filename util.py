import json
import os

def dict_from_json_file(filename):
	with open(filename, "r") as fileID:
		return json.loads(fileID.read())

def files_in_folder(folder_path):
	for _, _, files in os.walk(folder_path):
		return files
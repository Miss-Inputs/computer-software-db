#!/usr/bin/env python3

import json

def validate(path):
	with open(path, 'rt') as f:
		game_list = json.load(f)
	for game_name, game in game_list.items():
		if 'parent' in game:
			parent_name = game['parent']
			if parent_name in game_list:
				parent = game_list[parent_name]
				for key in parent.keys():
					if key == "notes":
						if key in game:
							game_list[game_name][key] = parent[key] + ";" + game_list[game_name][key]
						else:
							game_list[game_name][key] = parent[key]
					elif key not in game:
						game_list[game_name][key] = parent[key]
			else:
				print('Oh no! {0} refers to undefined parent game {1}'.format(game_name, parent_name))
			
	
validate('mac_db.json')
validate('dos_db.json')

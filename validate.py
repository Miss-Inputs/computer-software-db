#!/usr/bin/env python3

import json

valid_keys = ['parent', 'creator_code', 'app_name', 'other_app_names', 'arch', 'category', 'clone_of', 'notes', 'resolution_compat', 'colours_compat', 'width', 'notes', 'width', 'height', 'colours', 'min_players', 'max_players', 'controls', 'runs_in_window', 'genre', 'subgenre', 'developer', 'publisher', 'year', 'compat_notes', 'requires_cd', 'adult', 'emu_compat', 'required_hardware', 'required_software']
valid_arch = ['68k', 'ppc', 'fat']
valid_resolution_compat = ['empty_space', 'nag', 'required']
valid_colour_compat = ['palette', 'nag', 'required']


def read_game_list(path):
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
				
	return game_list

def validate(path):
	game_list = read_game_list(path)
	for game_name, game in game_list.items():
		for k, v in game.items():
			if k not in valid_keys:
				print(game_name, 'has invalid key:', k)
				
		#TODO: Check individual field values are valid
	
validate('mac_db.json')
validate('dos_db.json')

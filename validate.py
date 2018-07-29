#!/usr/bin/env python3

import json
import sys

valid_keys = ['parent', 'creator_code', 'app_name', 'other_app_names', 'arch', 'category', 'clone_of', 'notes', 'resolution_compat', 'colours_compat', 'notes', 'width', 'height', 'colours', 'min_players', 'max_players', 'controls', 'runs_in_window', 'genre', 'subgenre', 'developer', 'publisher', 'year', 'compat_notes', 'requires_cd', 'adult', 'emu_compat', 'required_hardware', 'required_software']
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
						
		if 'arch' in game and game['arch'] not in valid_arch:
			print(game_name, 'has invalid arch:', game['arch'])
		if 'resolution_compat' in game and game['resolution_compat'] not in valid_resolution_compat:
			print(game_name, 'has invalid resolution_compat:', game['resolution_compat'])
		if 'colour_compat' in game and game['colour_compat'] not in valid_colour_compat:
			print(game_name, 'has invalid colour_compat:', game['colour_compat'])
			
		if 'other_app_names' in game and not isinstance(game['other_app_names'], list):
			print(game_name, 'has invalid other_app_names:', game['other_app_names'])
		if 'width' in game and not isinstance(game['width'], int):
			print(game_name, 'has invalid width:', game['width'])
		if 'height' in game and not isinstance(game['height'], int):
			print(game_name, 'has invalid height:', game['height'])
		if 'colours' in game and not isinstance(game['colours'], int):
			print(game_name, 'has invalid colours:', game['colours'])
		if 'min_players' in game and not isinstance(game['min_players'], int):
			print(game_name, 'has invalid min_players:', game['min_players'])
		if 'max_players' in game and not isinstance(game['max_players'], int):
			print(game_name, 'has invalid max_players:', game['max_players'])
		if 'controls' in game and not isinstance(game['controls'], dict):
			print(game_name, 'has invalid controls:', type(game['controls']))
		if 'year' in game and not isinstance(game['year'], int):
			print(game_name, 'has invalid year:', game['year'])
		if 'runs_in_window' in game and not isinstance(game['runs_in_window'], bool):
			print(game_name, 'has invalid runs_in_window:', game['runs_in_window'])
		if 'requires_cd' in game and not isinstance(game['requires_cd'], bool):
			print(game_name, 'has invalid requires_cd:', game['requires_cd'])
		if 'adult' in game and not isinstance(game['adult'], bool):
			print(game_name, 'has invalid adult:', game['adult'])
		if 'emu_compat' in game and not isinstance(game['emu_compat'], dict):
			print(game_name, 'has invalid emu_compat:', type(game['emu_compat']))
		if 'required_hardware' in game and not isinstance(game['required_hardware'], dict):
			print(game_name, 'has invalid required_hardware:', type(game['required_hardware']))
		if 'required_software' in game and not isinstance(game['required_software'], dict):
			print(game_name, 'has invalid required_software:', type(game['required_software']))

		#TODO: Check "controls" object which will probably be tricky
		if 'emu_compat' in game:
			for k, v in game['emu_compat'].items():
				if not isinstance(v, bool):
					print(game_name, 'has invalid emu_compat.emulator', k, v)
					
		if 'required_hardware' in game:
			for k, v in game['required_hardware'].items():
				if k not in ('free_ram', 'cpu', 'cpu_speed', 'for_xt'):
					print(game_name, 'has invalid required_hardware key', k)
				
			if 'free_ram' in game['required_hardware']:
				if not isinstance(game['required_hardware']['free_ram'], int):
					print(game_name, 'has invalid required_hardware.free_ram', game['required_hardware']['free_ram'])
			if 'cpu_speed' in game['required_hardware']:
				if not isinstance(game['required_hardware']['cpu_speed'], (int, float)):
					print(game_name, 'has invalid required_hardware.cpu_speed', game['required_hardware']['cpu_speed'])
			if 'for_xt' in game['required_hardware']:
				if not isinstance(game['required_hardware']['for_xt'], bool):
					print(game_name, 'has invalid required_hardware.for_xt', game['required_hardware']['for_xt'])
					
		if 'required_software' in game:
			for k, v in game['required_software'].items():
				if k not in ('os', 'os_version', 'extensions'):
					print(game_name, 'has invalid required_software key', k)
				
			if 'extensions' in game['required_software']:
				if not isinstance(game['required_software']['extensions'], list):
					print(game_name, 'has invalid required_software.extensions', game['required_software']['extensions'])

def check_missing(path, key):
	game_list = read_game_list(path)
	for game_name, game in game_list.items():
		if key not in game:
			print(path, '->', game_name, 'missing', key)

def check_missing_metadata(path):
	game_list = read_game_list(path)
	for game_name, game in game_list.items():
		for key in {'category', 'genre', 'subgenre', 'year'}:
			if key not in game:
				print(path, '->', game_name, 'missing', key)
		if 'developer' not in game and 'publisher' not in game:
			print(path, '->', game_name, 'missing developer/publisher')

if len(sys.argv) > 1:
	arg = sys.argv[1]
	if arg == 'metadata':
		check_missing_metadata('mac_db.json')
		check_missing_metadata('dos_db.json')
	elif arg not in valid_keys:
		print('Key not valid:', arg)
	else:
		check_missing('mac_db.json', arg)
		check_missing('dos_db.json', arg)
else:
	validate('mac_db.json')
	validate('dos_db.json')

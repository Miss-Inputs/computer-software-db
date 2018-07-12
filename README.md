# computer-software-db

Eh, how to describe things...

Contains controls, compatibility, category, and other things starting with c for software for computers that require installing stuff or putting things in folders or stuff, rather than running everything directly from external media (which would be a lot easier to organize).

Currently targets Mac (68K) and DOS. Windows 3.1 and PPC Mac (OS 8/9) are intended to follow as well, but I would also add any other platform where it becomes relevant.

It's mainly intended for emulation, but I suppose you could use it for real hardware if you have some creative way of doing that. But it's mainly so that launchers for games on these platforms can have controls mapped and configure emulators automatically and whatnot.

It'll make sense when it's used, I guess.

### Data structure thingo:

Subject to change, but for now:

- name: Display name of the game/app; stuff in brackets denotes different versions etc
- creator_code: For Mac: creator code of the game/app; used for identification purposes
- app_name: Actual filename of the game/app; used for identification purposes where creator_code is ambiguous
- other_app_names: Other names of the game/app for identification purposes, such as other versions that work the same way
- arch: For Mac, CPU architecture: "68k", "ppc", "fat" Hmm... maybe could use "x86_16" and "x86_32" or something like that for Windows?
- category: Category of the app: "Games", "Applications", etc
- clone_of: What existing game this is a clone of, if applicable
- notes: Comment about the game or whatever, sometimes this is just a sign I need more fields instead of putting everything in here
- resolution_compat: Reason for resolution being specified:
	- "empty_space": Game will have black borders and whatnot if run at a higher resolution than this
	- "nag": Game will nag if not run at the specified resolution
	- "required": Game will refuse to run if not using the specified resolution
	- If not specified, game should run at desktop resolution, or otherwise whatever the best resolution is
- colours_compat:
	- "nag": Game will nag if not run at the specified colour depth (e.g. "This game may run slowly!" etc), but still run
	- "required": Game will refuse to run if not using the specified colour depth
	- "palette": Game will run with the wrong colour palette and things will look trippy
	- If not specified, game should run at max colours
- width: Screen width that this game should run in
- height: Screen height that this game should run in
- colours: Amount of colours on screen that this game should run with (2, 16, 256, "thousands", "millions" etc)
- min_players: Minimum human players required to play this game, should be >1 (or should demos be considered to have 0 players? Or should start/quit/etc be considered controls?)
- max_players: Maximum human players that this game can be played with, should be >1 and <= min_players
- controls: Object:
	- player_x: Object (controls for player X, e.g. "player_1" = player 1 controls)
		- Any number of "action": ["key", "map_to"]
		- #TODO: Decide how this will store key = mouse, and map_to = analog
		- "action" is just the thing what you're doing in game, e.g "jump" "move_left" "fire"
		- "key" is what you're pressing on the emulated Mac, arrow keys are specified as "x_arrow", numpads are specified as "x_numpad": e.g. "a", "b", "up_arrow", "5_numpad"
		- "map_to" is what this should be ideally mapped to (using an abstracted controller layout), or null if the control scheme is too complex for that and would need some kind of manual configuration. Can be one of these:
			- "left_stick_up"
			- "left_stick_down"
			- "left_stick_left"
			- "left_stick_right"
			- "dpad_up"
			- "dpad_down"
			- "dpad_left"
			- "dpad_right"
			- "right_stick_up"
			- "right_stick_down"
			- "right_stick_left"
			- "right_stick_right"
			- "left_shoulder"
			- "right_shoulder"
			- "primary_button" #Should be lower face button on modern pads
			- "secondary_button" #Should be left face button on modern pads
			- "aux_primary_button" #Should be right face button on modern pads
			- "aux_secondary_button" #Should be upper face button on modern pads
			- "select"
			- "start"
			- "left_trigger_down"
			- "left_trigger_up"
			- "right_trigger_down"
			- "right_trigger_up"
			- "left_thumb_button"
			- "right_thumb_button"
- runs_in_window: For Mac and Windows: If true (default false), doesn't actually run in fullscreen. Hmm... how should this interact with resolution stuff?
- genre: Game genre, though applications can have genres too because I said so (Word Processor, Game Utility, etc) though of course this all isn't consistent
- subgenre: Game/app subgenre, again arbitrarily defined
- compat_notes: Other notes on compatibility, should be displayed to the user
- requires_cd: If true (default false), game requires the CD inserted in the drive to play the game
- adult: If true (default false), game is too pornographic for kids
- emu_compat: For Mac (since you don't have much choice with DOS, unless you want a convoluted solution that automatically generates disk images and boots them with some entire-PC emulator), compatibility with various emulators, object with any number of:
	- "emulator": value
		- Where emulator is: mame, mini_vmac, basilisk_ii, sheepshaver, qemu, dosbox
		- Hmm, do I want to add "classic_environment" "pce_macplus" and maybe "fusion" "executor" to that list? Or to separate mame into mame_macii etc?
		- value is: true, false (for now, gonna have a think about how partial incompatibility might work aside from just using compat_notes)
- required_hardware: Minimum hardware requirements (object):
	- "free_ram": Free RAM required in bytes
	- "cpu": CPU model
	- "cpu_speed": Minimum CPU speed in MHz
	- "for_xt": For DOS, specifies that this is designed for PC-XT or earlier (4.77MHz CPU) and will probably run too fast on a newer system
- required_software: Software requirements (object):
	- "os": Mac: Minimum System / Mac OS version required; DOS: "dos" or "win"
	- "os_version": DOS/Windows version (hmm, maybe I should just set this to "mac" for Mac games and use this for min system version)
	- "extensions": Mac: Array of extensions required

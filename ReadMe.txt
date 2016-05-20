Designed for highlevel rapid prototyping of node like processing. Inspired by the potential of IBM's TrueNorth Chip (and later on by the game TIS-100). Currently in the process of being rebuilt from the ground up.

Running it (once it's rebuilt enough to run):
	NPUEngine.py is the engine (can be run by itself to perform tests)
	import the engine, and initilize it as a class
	load the desired program (look in the examples folder for programs)
	write input, read output from engine (look at bottom of NPUEngine.py for examples/engine testing)

Changelog:
v0.11->v0.12:
	complete rebuild of engine from the ground up
	redefinition of what programs syntax should look like
v10->Git v0.11:
	Switchover to use of Git for version management //after a year of two of not touching this code... so many things to fix... and redesign...
	enabled debugging levels
	proper debugging enabled
	BUG unable to load programs from subdirectories properly

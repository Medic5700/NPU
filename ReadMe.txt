Designed for highlevel rapid prototyping of nural node like processing. 

Notes:
assumtion: an information unit is xor tuple, not type(None). A Node returns xor information unit, None, tuple
assumtion: when reads/writes to dataArray are zero per step, computation is finished
assumtion: some metaNodes have access to the engine variables, arrays contains all nodes, to enable dynamic rewiring of nodes
assumtion: each node completes execution after a bounded amount of time related to input
assumtion: A node can send one argument to many nodes, a node can RECIVE one argument from many nodes (First come, first serve) (IE: one argument can infact be reciveing data from multiple nodes)
assumtion: a node may recive feedback from another node, such feedback is required AND must be timely (IE: no batch processing input, if that node could be getting feedback from a node it's sending data to)

Changelog:
v10->Git v0.11:
	Switchover to use of Git for version management //after a year of two of not touching this code... so many things to fix...
	TODO add documentation to all functions
	TODO is a copy of baseNodes.py inside the main program?
	TODO enable automated testing
	TODO add proper debuging options
	BUG unable to load programs from subdirectories properly
v9->v10:
	TODO: Get execution statistics on nodes
	added ability to specify time to sleep between steps
v8->v9:
	Created some of the machenery needed to impliment 'metaNodes', created a metaNode class, created some variables related to executing metanodes, marked out a place to put code for metanodes
	BUG: relay nodes only relays data when all args have input?
	TODO: Copy and paste entire nural nets?
	added input/output fucntions for the engine
	added signal attribut to nodes, currently doesn't do anything
	changed name of io, wrapper, and meta attributs to something more fitting
	FIXED: relays executing every step when dimInput = 0
	Created new test programs
	end of execution now determined by I/O to dataArray instead of compairing new and old dataArrays
	FIXED: "Node validation complete" message given BEFORE nodes are unencapsulated, and therefore, validation confermation given before all nodes are validated
	FIXED: corrected error of passing tuple output args to incorrect input args
	DECISION: should encapsulating nodes have __enoughInput__()?
	FIXED: validation of nodes (and the filling in of missing info) happens after missing info is used to create routing table (def unencapsulate->tempRoutingTable = createRoutingTable(tempNodeList))
	Cleaning up code and adding some internal documentation
	FIXED: passing a single variable in causes engine to think execution is finished
	FIXED: doesn't check that all nodes are INITILIZED when adding them to nodeList
	Fixed: bakeInput requires name arg, name is optional
	Fixed: bakeInput only takes in list, not a single lone element
	TODO: one to all signaling
	//the rebuild was somehow completly successfull... much better then expected
v7->v8:
	...Screw it, I'm rebuilding it... (I'm gutting too much of it to even try anything short of rebuilding it)
	remade userprogrames to how they SHOULD be...?
	TODO: make metaclass
	TODO: make IO class/flag
	Started some documentation on how to actually use this thing
	TODO: way to measure activity across each connection
	TODO: turn the entirty of engine into a single modual that can be called from another python program
	TODO: make main program take input from calling args
	TODO: breakpoint node that displays what's passing through it, usefull for debugging
	TODO: completly remake datastructures. RoutingTable should be converted into a doubly linked list implimented as a porperty of each node in nodeList. DataTable should be implimented as an array corrisponding to the each node in nodeList.
v6->v7:
	made machinery for encapsulating Nodes... it kindof works on one test case, and it's messy... but I'll save it here
	functions used for making nodes and configuring routing table are now defined in a single class instead of as seperate functions
	removed some dead code
v5->v6:
	set up class Encapsulate for future use to make nural net function... type things... dynamically?
	Changed example/test programs to be more self contained
	TODO: allow importing of modules with functions that have the same name
	Improved verification helper functions
	Node verification now happens on initialized nodes instead of on uninitialized classes
	can now import multiple modules/nural functions from multiple files
	TODO: multithreading support
	included 'OPTIMIZATION' comments for guidence on future possible optimizations
	TODO: encapsulation of nodes
		make encapsolation node
		when encapsolation node encoutered, replace with forwarding node, append routing table from table provided by encapsolation node
	cleaned up commented out code
	FIXED: again...
		bug where importing and using multiple functions causes some functions to be overwritten	
v4->v5:
	Fixed: bug where importing and using multiple functions causes some functions to be overwritten
	basic nodeList verification to fix if dimInput or dimOutput variables of a node are missing
	verifiys routing table to gaurd ageinst multiple outputs being directed to a single input arg
	initializing Nodes and wiring them together now done in program1.py
	created debug variable
	better internal documentation
	more output showing configuration, blah blah blah
	Fixed: BaseNode is no longer parsed
	BUG: inheritence between classes causes parser to set incorrect values for dimInput
	-TODO: try to dynamically import nural programs
	TODO: investigate partial parsing? Maybe macros?, for setting routing table
	TODO: Contiguous block of input for functions
	TODO: parallel processing of nodes
v3->v4:
	cleaned up/reordered code (un-spegetti-fying my code)
	output can output to a file
	created Read Me.txt with change log and basic user instructions
	can now define size of required input for a class
	bug: when parsing classes, and calculating dimInput, assigning a value to baseNodes.Node->dimInput sets value for all subclasses parsed after it
		http://stackoverflow.com/questions/10064688/cant-access-parent-member-variable-in-python
	bug: intermitent crash when running NuralNet using imported functions (not classes), probibly related to previous bug
	can get and parse functions from user made file(in addition to classes) //still a WIP
	-TODO: implement a two stage initialization process
	TODO: make a flowchart to show how the program handles stuff (imports, and when stuff is done to what)
v2->v3:
	dynamically scalled arrays for function requirments
	functions can map to multiple nodes
	input can read from a file (or just bake the input/output)
	can get and parse classes from user made file
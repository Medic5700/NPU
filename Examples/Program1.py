#This is the goal of how the program will look if it's set up right?
#WIP

#Program1: Takes input, sums, returns output

#imports may work a little weird, as the source code is loaded and compiled dynamically
#reads and writes to a file will also be weird, as the source code is loaded and compiled dynamically, and all file references would be relative to the engine or calling file?
def sum(a,b):
    return a+b

class main(): #little to no inheritance
    """This is the main class, it's the class the engine runs to figure out how everything fits together"""
    def make(self, classList): #as few arguments as possible
        """takes a dictionary of nodes, initilizes nodes, returns dictionary of initialized nodes"""
        #classList contains all the functions and classes in this program, along with other defined nodes (relays, input/output, other engine specific stuff)
        
        ''' #the old way, not streamlined, and order mattered alot when it should not, required a fair bit of overhead
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['BakeInput']([i for i in range(20)],"2"))
        nodeList.append(classList['sum'])
        nodeList.append(classList['Output']("1"))
        '''
        
        ''' #one way to do it... but a little long
        nodeList = []
        nodeList.append(classList["input"]("input1")) #each node has a unique name, can use string or int for name
        nodeList.append(classList["input"]("input2")) #should be able to initialize inputs to start with a set of input, IE: [i for i in range(20)]
        nodeList.append(classList["sum"]("sum")) #even though this is a function, it should still have a unique name
        nodeList.append(classList["output"]("output1"))
        '''
        
        #this method forces a unique name for every node, alot more streamlined, and reinforces order doesn't matter
        nodeList = {}
        nodeList["input1"] = classList["input"]()
        nodeList["input2"] = classList["input"]()
        nodeList["sum"] = classList["sum"]()
        nodeList["output1"] = classList["output"]()
        
        #the nodes "in" and "out" are relays, automatically appended, used for recursion (should apply to root, for recursion reasons)
        return nodeList
    def routing(self):
        """outputs a dictionary of node i/o connections"""
        table = {} #instead of a multidimensionsal array, use a dictionary
        #you are saying which input connects to which output
        ''' #the original way, not user friendly in the least
        routingTable[1][3][0][0] = True
        routingTable[2][3][0][1] = True
        routingTable[3][4][0][0] = True
        '''
        
        ''' #this method doesn't specifiy which output argument the input argument connects to
        table["sum"] = ["input1","input2"] 
        table["output1"] = ["sum"]
        '''
        
        #more specific, more understandable, let you only put what you need, prevents multiple outputs to one input but allows multiple inputs from one output, not quite as streamlined? ([{BRACKETS!}]), allows easy additions to node routing information
        table["sum"] = {0:{"input1":0}, 1:{"input2":0}}
        table["output1"] = {0:{"sum":0}}
        return table

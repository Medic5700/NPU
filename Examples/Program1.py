#This is the goal of how the program will look if it's set up right? WIP
#Program1: Takes input, sums, returns output
def sum(a,b):
    return a+b

class main(): #little to no inheritance
    """This is the main class, it's the class the engine runs to figure out how everything fits together in this program"""
    def makeNet(self, classList): #as few arguments as possible
        """takes a dictionary of nodes, initilizes nodes, returns dictionary of initialized nodes"""
        nodeList = {}
        nodeList["input1"] = classList["input"]()
        nodeList["input2"] = classList["input"]()
        nodeList["sum"] = classList["sum"]()
        nodeList["output1"] = classList["output"]()

        table = {}
        table["sum"] = {0:{"input1":0}, 1:{"input2":0}}
        table["output1"] = {0:{"sum":0}}
        return nodeList,table

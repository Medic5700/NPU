#takes two inputs, adds them together, then subtracts that from input[1]
import baseNodes

def sum(a,b):
    return a+b

def sub(a,b):
    return a-b

class Main(baseNodes.Encapsulate):
    def makeNodes(self, nodeList, classList):
        #This tells in what order and how to initilize and populate the nodeList (order Matters)
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['sum'])
        nodeList.append(classList['sub'])
        nodeList.append(classList['Output']("1"))
    
    def configRouting(self, routingTable):
        #this configures the routingTable
        routingTable[1][3][0][0] = True
        routingTable[2][3][0][1] = True
        routingTable[1][4][0][0] = True
        routingTable[3][4][0][1] = True
        routingTable[4][5][0][0] = True

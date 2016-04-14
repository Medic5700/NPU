#program
#takes sums to inputs, then outputs result
import baseNodes

def sum(a,b):
    return a+b

class Main(baseNodes.Encapsulate):
    def makeNodes(self, nodeList, classList):
        #This tells in what order and how to initilize and populate the nodeList (order Matters)
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['BakeInput']([i for i in range(20)],"2"))
        nodeList.append(classList['sum'])
        #nodeList.append(classList['Output']("1"))
        nodeList.append(classList['Output']("1"))
    def configRouting(self, routingTable):
        #this configures the routingTable
        routingTable[1][3][0][0] = True
        routingTable[2][3][0][1] = True
        routingTable[3][4][0][0] = True    

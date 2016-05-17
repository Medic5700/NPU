#takes two inputs, adds them together, then subtracts that from input[1]
import baseNodes

def sum (a,b):
    #print("sum function\t=\t"+str(a)+" "+str(b))
    return a+b

class Test(baseNodes.Encapsulate):
    #built with the anticipation of adding support for encapsulated nodes =D
    def __init__(self):
        self.dimInput = 3
        self.dimOutput = 1
    
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['sum'])
        nodeList.append(classList['sum'])
    def configRouting(self, table):
        table[0][1][0][0] = True
        table[0][1][1][1] = True
        table[1][2][0][1] = True
        table[0][2][2][0] = True
        table[2][3][0][0] = True        

class Main(baseNodes.Encapsulate):
    #built with the anticipation of adding support for encapsulated nodes =D
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['BakeInput']([i for i in range(20)],"2"))
        nodeList.append(classList['BakeInput']([i for i in range(20)],"3"))
        nodeList.append(classList['Test']())
        nodeList.append(classList['Output']("1"))
    def configRouting(self, table):
        table[1][4][0][0] = True
        table[2][4][0][1] = True
        table[3][4][0][2] = True
        table[4][5][0][0] = True

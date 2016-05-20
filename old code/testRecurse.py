#this tests max recursion depth, assuming recruse limit set to 200
import baseNodes

class Test(baseNodes.Encapsulate):
    #built with the anticipation of adding support for encapsulated nodes =D
    def __init__(self, x):
        self.dimInput = 1
        self.dimOutput = 1
        self.temp = x
    
    def makeNodes(self,nodeList,classList):
        if self.temp>0:
            nodeList.append(classList['Test'](self.temp-1))
    def configRouting(self, table):
        if self.temp>0:
            table[0][1][0][0] = True
            table[1][2][0][0] = True
        else:
            table[0][1][0][0] = True

class Main(baseNodes.Encapsulate):
    def __init__(self):
        self.x = 256
    
    #built with the anticipation of adding support for encapsulated nodes =D
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['Test'](self.x-2))
        nodeList.append(classList['Output']("1"))
    def configRouting(self, table):
        table[1][2][0][0] = True
        table[2][3][0][0] = True

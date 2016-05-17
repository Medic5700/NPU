#tests the step limit, assuming it's set to 200
import baseNodes

class Main(baseNodes.Encapsulate):
    def __init__(self):
        self.x = 256
    
    #built with the anticipation of adding support for encapsulated nodes =D
    def makeNodes(self,nodeList,classList):
        #nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['BakeInput'](0,"1"))
        for i in range(self.x-2):
            nodeList.append(classList['Relay'](1))
        nodeList.append(classList['Output']("1"))
    def configRouting(self, table):
        for i in range(self.x-2+2):
            table[i][i+1][0][0] = True

#tests that passing arguments between nodes works for all casses
import baseNodes

class testSinglePass(baseNodes.Encapsulate):
    def __init__(self):
        self.dimInput = 1
        self.dimOutput = 0
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['Output']("testSingle"))
    def configRouting(self,table):
        table[0][1][0][0] = True

class test2MultipleNodes(baseNodes.Encapsulate):
    def __init__(self):
        self.dimInput = 1
        self.dimOutput = 0
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['sum'])        
        nodeList.append(classList['Output']("test2MultipleNodes"))
    def configRouting(self,table):
        table[0][1][0][0] = True
        table[0][1][0][1] = True
        table[0][1][0][2] = True
        table[1][2][0][0] = True
def sum(a,b,c):
    return a+b+c

class testInputOverload(baseNodes.Encapsulate):
    def __init__(self):
        self.dimInput = 1
        self.dimOutput = 0
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['sum'])        
        nodeList.append(classList['Output']("testInputOverload"))
    def configRouting(self,table):
        table[0][1][0][0] = True
        table[0][1][0][1] = True
        table[0][1][0][2] = True
        
        table[0][2][0][0] = True
        table[1][2][0][0] = True

class testMultiArgs(baseNodes.Encapsulate):
    def __init__(self):
        self.dimInput = 1
        self.dimOutput = 0
    def makeNodes(self,nodeList,classList):      
        nodeList.append(classList['Output']("testInputOverload"))
    def configRouting(self,table):
        table[0][1][0][0] = True
        table[0][1][0][1] = True
        table[0][1][0][2] = True
        
        table[0][2][0][0] = True
        table[1][2][0][0] = True
class duMux(baseNodes.BaseNode):
    def __init__(self):
        self.direction = 0
        self.dimInput = 1
        self.dimOutput = 4
    def main(self,x):  
        output = [None,None,None,None]
        output[self.x] = x
        self.x = (self.x+1)%4
        return tuple(output)

class Main(baseNodes.Encapsulate):
    #built with the anticipation of adding support for encapsulated nodes =D
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        nodeList.append(classList['testSinglePass']())
        nodeList.append(classList['test2MultipleNodes']())
        nodeList.append(classList['testInputOverload']())
    def configRouting(self, table):
        table[1][2][0][0] = True
        table[1][3][0][0] = True
        table[1][4][0][0] = True
        
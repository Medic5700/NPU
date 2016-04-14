#one input to multiple outputs
import baseNodes
class Split4(baseNodes.BaseNode):
    #a test node, to experiment with
    dimOutput = 4
    
    output = [None,None,None,None]
    
    def main(self,a):
        self.dimOutput = 4
        temp = self.output.index(None)
        self.output[temp] = a
        if temp == 3:
            temp2 = (self.output[0],self.output[1],self.output[2],self.output[3])
            self.output = [None,None,None,None]
            return temp2
        else:
            return None

class Main(baseNodes.Encapsulate):
    def makeNodes(self, nodeList, classList):
        nodeList.append(classList['BakeInput']([i for i in range(20)],"1"))
        #nodeList.append(classList['Input']("1","test.txt"))
        nodeList.append(classList['Output']())
        nodeList.append(classList['Output']("2"))
        nodeList.append(classList['Output']("3"))
        nodeList.append(classList['Output']("4"))
        #nodeList.append(classList['Output']("4","test2.txt"))
        nodeList.append(classList['Split4']())
    
    def configRouting(self, routingTable):
        routingTable[1][6][0][0] = True
        routingTable[6][2][0][0] = True
        routingTable[6][3][1][0] = True
        routingTable[6][4][2][0] = True
        routingTable[6][5][3][0] = True 
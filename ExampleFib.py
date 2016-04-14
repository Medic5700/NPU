import baseNodes

class t1(baseNodes.BaseNode):
    def __init__(self,start):
        self.dimInput = 3
        self.dimOutput = 2
        self.temp = start
        
    def main(self, i, j, k):
        #i is the recruse counter, j and k is the output/input to sum
        if i>0:
            return tuple((i-1,j+k))
        else:
            return None

class fib(baseNodes.Encapsulate):
    #built with the anticipation of adding support for encapsulated nodes =D
    def __init__(self):
        self.dimInput = 1
        self.dimOutput = 1
    
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['t1'](0))
        nodeList.append(classList['t1'](0))
        nodeList.append(classList['t1'](1))
        nodeList.append(classList['BakeInput']([0],"fibInit"))
        nodeList.append(classList['BakeInput']([1],"fibInit2"))
    def configRouting(self, table):
        #init
        table[0][1][0][0] = True
        table[4][1][0][1] = True
        table[4][1][0][2] = True
        table[5][2][0][1] = True

        #token passing
        table[1][2][0][0] = True    
        table[2][3][0][0] = True 
        table[3][1][0][0] = True 
        
        #sending numbers
        table[1][2][1][2] = True  
        table[2][3][1][2] = True 
        table[3][1][1][2] = True 
        
        table[1][3][1][1] = True  
        table[2][1][1][1] = True 
        table[3][2][1][1] = True         
        
        #output
        table[1][6][1][0] = True 
        table[2][6][1][0] = True 
        table[3][6][1][0] = True 
        
class Main(baseNodes.Encapsulate):
    #built with the anticipation of adding support for encapsulated nodes =D
    def makeNodes(self,nodeList,classList):
        nodeList.append(classList['BakeInput']([10]))
        nodeList.append(classList['fib']())
        nodeList.append(classList['Output']())
    def configRouting(self, table):
        table[1][2][0][0] = True
        table[2][3][0][0] = True
        
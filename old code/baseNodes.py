#caution, inheritence between classes can cause problems with setting dimInput/dimOutput
import functools

class BaseNode:
    #this is a dummy node (is not parsed), can be inherited, shows what is used/needed to work with program
    #dimInput = None #dimension of input, is set by functionParsing.dimInput, can be manually set
    #dimOuput = None #dimension of output, set to zero if not specified
    #wrapper = None #used to determine if a node is a function, to be futher anylsed by parser?
    #isIO
    #isMeta
    #signal = []
    
    def __init__(self):
        pass
    def __enoughInput__(self,x):
        #takes a tuple of input (which can contain None, to mean no data for that arg), and returns true/false if that input is enough to run main
        temp = True
        for i in range(self.dimInput):
            if x[i] == None:
                temp = False
        return temp
    def main(self):
        #runs every time __enoughInput__ returns true, with number of arguments equal to dimInput
        pass
        
class BakedNode(BaseNode):
    #used to convert a function into a node class
    def __init__(self,f,i,o):
        self.function = f
        self.dimInput = i
        self.dimOutput = o
    def main(self,*x):
        partialFunction = functools.partial(self.function)
        for j in x:
            partialFunction = functools.partial(partialFunction,j)
        return partialFunction()

class InputOutput(BaseNode):
    #a placeholder for an I/O class
    isIO = True
    def close(self):
        pass   

class Input(InputOutput):
    #takes input from a file
    dimOutput = 1 #this line 'should' be in __init__, but can be placed here, may cause trouble if another class inherits this one
    def __init__(self,x,name=""):
        self.read = False
        self.file = open(x, "r", encoding="utf-8")
        self.name = name
    def main(self):
        if self.read == False:
            self.read = True
            output = []
            for i in self.file.read().split():
                output.append((i))
            self.file.close()
            print("Input["+str(self.name)+"]\t=\t"+str(output))
            return output
        else:
            return None

class BakeInput(InputOutput):
    #outputs data from when it was initialized, good for testing
    dimOutput = 1
    def __init__(self,x,name=""):
        self.read = False        
        self.data = x
        self.name = name
    def main(self):
        if self.read == False:
            self.read = True
            output = []
            if type(self.data)==type([]):
                for i in self.data:
                    output.append((i))
            else:
                output.append(self.data)
            print("BakeInput["+str(self.name)+"]\t=\t"+str(output))
            return output
        else:
            return None    
    
class Output(InputOutput):
    #outputs to screen and optionally to a file
    def __init__(self,name="",destination=None):
        self.dimInput = 1
        self.dimOutput = 0
        self.name=name
        if destination != None:
            self.file = open(destination, "w", encoding="utf-8")
        else:
            self.file = None
    def __enoughInput__(self,x):
        return x[0] != None
    def main(self,x):
        print("output["+str(self.name)+"]\t=\t"+str(x))
        if self.file != None:
            self.file.write(str(x)+"\n")
    def close(self):
        if self.file != None:
            self.file.close()
            
class Encapsulate(BaseNode):
    #built with the anticipation of adding support for encapsulated nodes =D
    isWrapper = True #used to specifiy that this is an encapsulation node
    def __init__(self):
        self.dimInput = None
        self.dimOutput = None
    ''' #omitted so error will be raised if these are missing
    def makeNodes(self,NodeList,classList):
        pass
    def configRouting(self, table):
        pass
    '''
class Relay(BaseNode):
    #ment to be a relay to forward input to another Node, used in conjunction with 'Encapsulate'
    def __enoughInput__(self,x):
        if self.dimInput>0:
            temp = True
            for i in range(self.dimInput):
                if x[i] == None:
                    temp = False
            return temp
        else:
            return False

    def __init__(self,i,name=""):
        self.dimInput = i
        self.dimOutput = i
        self.name = name
    #__enoughInput__ would be replaced by the encapsulating node's __enoughInput__
    def main(self,*x):
        #print("relay "+str(self.nid)+"\t=\t" + str(x))
        
        output = []
        for i in range(self.dimInput):
            output.append(x[i])
        #print("relay x output\t=\t" + str(output))
        #print("\tdimInput="+str(self.dimInput)+"\tdimOutput="+str(self.dimOutput)+"\toutput="+str(output))
        return tuple(output)
    
class Meta(BaseNode):
    isMeta = True
    def meta(self, nodeList, classList, dataArray, functions):
        pass
    
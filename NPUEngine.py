import inspect # https://docs.python.org/3.4/library/inspect.html
import copy # https://docs.python.org/2/library/copy.html
import functools # http://stackoverflow.com/questions/3188048/how-to-bind-arguments-to-given-values-in-python-functions
import baseNodes
import time # https://docs.python.org/3.4/library/time.html

_VersionNumber = "v0.11"

#User changable options
toImport = ["ExampleProgram1"] #list of modules to import for makeing the Nural Net
debug = False #enables display of additional data
debugMode = True #enables debug logging
recursionDepth = 256 #the depth that encapsulated nodes will be parsed, only used for nodeList initialization
stepLimit = 256 #controls how many 'steps' a program can take at most
stepDelay = 0.0 #seconds to delay between steps, a real

#Other options
debugLevel = 0 #the level of detail to log, higher is more detailed
debugOutput = "NPUEngine.log"

#-------------------------------------------------------------------------------
class Debug:
    """Class for logging and debuging"""
    def __init__(self, debugMode, level=0, file="NPUEngine.log"):
        self.__filename = file
        self.showDebug = debugMode #Bool
        self.level = level
        
    def __save(self, text):
        """Function to save each log entry"""
        logfile = open(self.__filename, 'a')
        try:
            logfile.write(text)
        except:
            self.err("Error Occured in Error Logging Function: Attempting to report previous error")
            for i in text:
                try:
                    logfile.write(i)
                except:
                    logfile.write("[ERROR]")
        logfile.close()

    def log(self, text):
        """Takes string, pushes to stdout AND saves it to the log file
        
        For general logging, and non-fatal errors
        """
        temp = "[" + time.asctime() + "] Log: " + text
        print(temp)
        self.__save(temp + "\n")
    
    def err(self, text):
        """Takes string, pushes to stdout and saves it to the log file
        
        Mainly meant for non-recoverable errors that should cause the program to terminate"""
        temp = "[" + time.asctime() + "] ERR: " + text
        print(temp)
        self.__save(temp + "\n")        
    
    def debug(self, *args):
        """takes n number of strings, pushes to stdout and log file
        
        only writes input to stdout/log file when showDebug is True"""
        if (self.showDebug):
            temp = "Debug0:"
            for i in args:
                temp += "\t" + str(i) + "\n"
            print(temp, end="") #fixes issue where log and sceen output newlines don't match
            self.__save(temp)
            
    def debug1(self, *args):
        """takes n number of strings, pushes to stdout and log file
        
        only writes input to stdout/log file when showDebug is True
        Level 1 debuging"""
        if (self.showDebug and (self.level >= 1)):
            temp = "Debug1:"
            for i in args:
                temp += "\t" + str(i) + "\n"
            print(temp, end="") #fixes issue where log and sceen output newlines don't match
            self.__save(temp)
            
error = Debug(debugMode, debugLevel, debugOutput) #initialize debuging

error.log("Starting NPUEngine " + _VersionNumber + " ==========================================")
#imports functions from other files
_modules = []
for i in toImport: # http://stackoverflow.com/questions/951124/dynamic-loading-of-python-modules
    _modules.append(__import__(i))

_classList = {} #contains a list of classes that can be used to make nodes
_nodeList = {} #contains a list of initialized nodes, to be executed, identified by nid

class Input (baseNodes.BaseNode):
    def __init__(self,name=""):
        self.isIO=True
        self.name=name
        self.data=[]
        self.dimOutput=1
    def __enoughInput__(self,x):
        return len(self.data)>0
    def main(self):
        output = []
        for i in self.data:
            output.append(i)
        return output
    def close(self):
        pass
    def write(self,x):
        try:
            if type(x)==type([]):
                for i in x:
                    self.data.append(i)
            else:
                self.data.append(x)
            return True
        except:
            return False

class Output(baseNodes.BaseNode):
    def __init__(self,name=""):
        self.isIO=True
        self.name=name
        self.data=[]
        #self.dimInput=1
    def __enoughInput__(self,x):
        return x!=None
    def main(self,x):
        self.data.append(x)
    def close(self):
        pass
    def read(self):
        if len(self.data)>0:
            return self.data.pop(0)
        else:
            return None

engineInput = Input("engineInput")
engineOutput = Output("engineOutput")

#-------------------------------------------------------------------------------
def validateNodes(x):
    """
    parses a dictionary of nodes, checks if nodes have basic required functions, sets variables if needed
    returns true if nodes are verified
    """
    
    for i in x:
        if inspect.isclass(x[i]):
            error.err(" ERROR: "+str(x[i])+" is not initilized")
            exit(-1)
        
        temp = None
        #verifies required variables exist
        try:
            temp = x[i].dimInput
        except:
            x[i].dimInput = None
        try:
            temp = x[i].dimOutput
        except:
            x[i].dimOutput = None
            
        try:
            temp = x[i].isWrapper
        except:
            x[i].isWrapper = None
        try:
            temp = x[i].isIO
        except:
            x[i].isIO = None            
        try:
            temp = x[i].isMeta
        except:
            x[i].isMeta = None                
        
    
        try:
            temp = x[i].pointerInput
        except:
            x[i].pointerInput = None                
        try:
            temp = x[i].pointerOutput
        except:
            x[i].pointerOutput = None              
        try:
            temp = x[i].nid
        except:
            x[i].nid = None   
            
        try:
            temp = x[i].signal
        except:
            x[i].signal = None        
            
        #sets required variables if not set
        if x[i].dimInput==None:
            for j in inspect.getmembers(x[i]):
                if j[0]=='main':          
                    x[i].dimInput=len(inspect.getargspec(j[1])[0])-1     
        if x[i].dimOutput==None:
            x[i].dimOutput=0
            
        if x[i].isWrapper==None:
            x[i].isWrapper=False
        if x[i].isIO==None:
            x[i].isIO=False
        if x[i].isMeta==None:
            x[i].isMeta=False            
        if x[i].pointerInput==None:
            x[i].pointerInput=[]
        if x[i].pointerOutput==None:
            x[i].pointerOutput=[]
        if x[i].signal==None:
            x[i].signal=[]
            
        #verifies required esential internal functions exist, fatal errors
        try:
            temp = x[i].main
        except:
            error.err("\t\tERROR: node "+str(i)+", object "+str(x[i])+" is missing 'main'")
            exit(-1)
            
        try:
            temp = x[i].__enoughInput__
        except:
            #print("\t\tERROR: node "+str(x[i])+"missing '__enoughInput__'")
            error.err("\t\tERROR: node "+str(i)+", object "+str(x[i])+" is missing '__enoughInput__'")
            exit(-1)
        
        if x[i].isIO:
            try:
                temp = x[i].close
            except:
                error.err("\t\tERROR: node "+str(i)+", object "+str(x[i])+" is missing 'close'")
                exit(-1)        
                
        if x[i].isWrapper:
            try:
                temp = x[i].makeNodes
            except:
                error.err("\t\tERROR: node "+str(i)+", object "+str(x[i])+" is missing 'makeNodes'")
                exit(-1)                 
            try:
                temp = x[i].configRouting
            except:
                error.err("\t\tERROR: node "+str(i)+", object "+str(x[i])+" is missing 'configRouting'")
                exit(-1)                 
        error.debug("  "+ str(x[i]) + " dimInput:" + str(x[i].dimInput) + " dimOutput:" + str(x[i].dimOutput))
            
    return True
    
class functionParsing:
    def getClasses(x):
        #parses a given module for classes
        for i in inspect.getmembers(x):
            if inspect.isclass(i[1]):
                _classList[i[0]] = i[1]
                
    def getFunctions(x):
        #parses a given module for functions, then converts them to a class to be used in nodeList
        temp = {}
        for i in inspect.getmembers(x):
            if inspect.isfunction(i[1]):
                temp[i[0]] = i[1]
        error.log(" Processing imported functions = " + str(temp))
        for i in temp:
            t1 = baseNodes.BakedNode(temp[str(i)],len(inspect.getargspec(temp[i])[0]),1)
            _classList[str(i)] = t1
            error.debug(" Processing Function: "+str(i))    
                
#-------------------------------------------------------------------------------
#gets the functions from the imported source files, and populates the list
error.log("Parsing Classes/Functions")
functionParsing.getClasses(baseNodes)
_classList.pop("BaseNode") #removes "BaseNode" from list, helps fix inheritence issue when setting dimInput
for i in _modules:
    functionParsing.getClasses(i)
    functionParsing.getFunctions(i)

error.log(" Imported classes = "+str(_classList))

#-------------------------------------------------------------------------------
error.log("Starting Population of Node List")

nids = [0] #SHORTCUT: This should be in it's own class
class NID:
    def newNID():
        #generates and returns a new NID for a node
        nids.sort()
        temp = nids[len(nids)-1] + 1 #shortcut: should really be using some sort of randomization function here, especially once the program can dynamically generate nodes
        nids.append(temp)
        return temp

def createRoutingTable(nodeList):
    tempDim = 0
    for i in nodeList:
        if nodeList[i].dimInput > tempDim:
            tempDim = nodeList[i].dimInput 
        if nodeList[i].dimOutput > tempDim:
            tempDim = nodeList[i].dimOutput          
    return [[[[ False for i in range(tempDim)] for i in range(tempDim)] for i in range(len(nodeList.keys()))] for j in range(len(nodeList.keys()))]    

def unencapsulate(nodeList, classList, depth, ismain=False):
    '''
    General algorithm:
    takes dictionary of nodes
    scans nodes for wrappers
    takes wrappers:
        creates new list -> temp
        adds relays
        populated temp with nodes
        gets wiring of nodes in temp
        copies nodes in temp to dictionary temp2
        wires nodes in temp2 based on wireing in temp
        recurse on temp2
        merge temp2 and original dictionary of nodes
        rewire references to wrapper in dictionary of node to relays in temp
        pop wrapper
    '''    
    if depth>recursionDepth:
        error.err("\tError: Max Recusion depth reach, depth=" + str(depth))
        exit(-1)
    
    #getting around the 'can't modify the dictionary you are currently itterating over' error
    keys = []
    for i in nodeList.keys():
        keys.append(i)
        
    for i in keys:
        if nodeList[i].isWrapper:
            tempNodeList = []
            tempRoutingTable = None
            tempNIDS = [] #contains the NIDs of the temp nodes IN ORDER
            middleNodeList = {} #an intermediary between tempNodeList and _nodeList (in format)
            
            current = nodeList[i]
            del(nodeList[i])
            startNID = None #used to mark the start and end points of an encapsulated node
            endNID = None
                        
            current.makeNodes(tempNodeList,classList)
            if ismain==True: #inserts input/output nodes in the case it's the root main
                tempNodeList.insert(0,engineInput)
                tempNodeList.append(engineOutput)
            else:
                tempNodeList.insert(0,classList['Relay'](current.dimInput))
                tempNodeList.append(classList['Relay'](current.dimOutput))                

            for i in range(len(tempNodeList)):
                temp = NID.newNID()
                tempNIDS.append(temp)
                
                middleNodeList[temp] = copy.deepcopy(tempNodeList[i])
                middleNodeList[temp].nid = temp
                
            startNID = tempNIDS[0]
            endNID = tempNIDS[len(tempNIDS)-1]
                
            if not(validateNodes(middleNodeList)):
                error.err("\tError: Node Validation Failed -> " + str(_nodeList))
                exit(-1)                
            
            #creates routing table
            tempRoutingTable = createRoutingTable(middleNodeList)
            current.configRouting(tempRoutingTable)            
                
            for i in range(len(tempRoutingTable)):
                for j in range(len(tempRoutingTable[i])):
                    for k in range(len(tempRoutingTable[i][j])):
                        for l in range(len(tempRoutingTable[i][j][k])):
                            if tempRoutingTable[i][j][k][l]:
                                middleNodeList[tempNIDS[i]].pointerOutput.append([tempNIDS[i],tempNIDS[j],k,l]) #adds a pointer to destination in source Node
                                middleNodeList[tempNIDS[j]].pointerInput.append([tempNIDS[i],tempNIDS[j],k,l]) #adds a pointer to source in destination Node
            
            unencapsulate(middleNodeList,classList,depth+1)
            for i in middleNodeList:
                nodeList[i] = middleNodeList[i]
            
            #rewire reference to relays
            nodeList[startNID].pointerInput=current.pointerInput
            nodeList[endNID].pointerOutput=current.pointerOutput
            #changes references from nodes outside encapsulation to relays
            for i in current.pointerInput:
                for j in nodeList[i[0]].pointerOutput:
                    if j[1]==current.nid:
                        j[1]=startNID
            for i in current.pointerOutput:
                for j in nodeList[i[1]].pointerInput:
                    if j[0]==current.nid:
                        j[0]=endNID                        
            #changes relay pointers to correct nids
            for i in nodeList[startNID].pointerInput:
                i[1]=startNID
            for i in nodeList[endNID].pointerOutput:
                i[0]=endNID
                
_nodeList[0]=_classList["Main"]()
_nodeList[0].nid=0
_nodeList[0].dimInput=0 #Shortcut: allows unencapsulate to work without special code for base case
_nodeList[0].dimOutput=0
if validateNodes(_nodeList):
    error.log(" Main Node Validation complete")
else:
    error.err(" Error: Main Node Validation Failed, please check Main node")
    exit(-1)
unencapsulate(_nodeList, _classList, 0, True)

if validateNodes(_nodeList):
    error.log(" Node Validation complete")
else:
    error.err(" Error: Node Validation Failed -> " + str(_nodeList))
    exit(-1)
error.log(" Number of nodes = "+str(len(_nodeList.keys())))
#-------------------------------------------------------------------------------
#data Tables
error.log("Creating Data Tables")

def dataInit(data, nodeList):
    for i in nodeList.keys():
        data[i] = [[] for j in range(nodeList[i].dimInput)]

def mergeData(data1, data2):
    #appends data2 to data1
    for i in data1.keys():
        for j in range(len(data2[i])):
            if len(data2[i][j])>0:            
                for k in range(len(data2[i][j])):
                    data1[i][j].append(data2[i][j].pop(0))
                
def getData(key, data, nodeList, pop):
    global _ioDelta

    temp = [None for i in range(nodeList[key].dimInput)]
    for i in range(nodeList[key].dimInput):
        if len(data[key][i])>0:
            if pop:
                temp[i] = data[key][i].pop(0)
                _ioDelta += 1
            else:
                temp[i] = data[key][i][0]
    return temp
                
def setData(key, dataArray, nodeList, data):
    global _ioDelta
    
    if type(data)==type(None):
        pass
    elif type(data)==type([]):
        for i in data:
            setData(key, dataArray, nodeList, i)
    elif type(data)==type(tuple((1,2,3))):
        for i in range(nodeList[key].dimOutput):
            for j in nodeList[key].pointerOutput:
                if i==j[2]:
                    dataArray[j[1]][j[3]].append(data[i])
                    _ioDelta += 1
    else:
        _ioDelta += 1
        for j in nodeList[key].pointerOutput:
            dataArray[j[1]][j[3]].append(data) 
            
_ioDelta = None
_data = {}
_dataDelta = {}

dataInit(_data,_nodeList)
dataInit(_dataDelta,_nodeList)
#-------------------------------------------------------------------------------
#Code for metaNode accessable functions
_metaToolBox = {}

#-------------------------------------------------------------------------------
error.log("Starting net execution")
_ioDelta = 1
_step = 0
_startTime = 0
_endTime = time.clock()
while (_step < stepLimit) and (_ioDelta>0):
    error.debug("_step = " + str(_step))
    
    _ioDelta = 0
    _step +=1
    _startTime = time.clock()
    
    #executes all nodes (if applicable)
    for i in _nodeList.keys():
        if _nodeList[i].__enoughInput__(getData(i,_data,_nodeList,False)):
            args = getData(i,_data,_nodeList,True)
            partialFunction = functools.partial(_nodeList[i].main)
            for x in range(_nodeList[i].dimInput):
                partialFunction = functools.partial(partialFunction,args[x])
            output = partialFunction()
            setData(i,_dataDelta,_nodeList, output)
          
    error.debug1(" i/o = " + str(_ioDelta))    
    error.debug1(" dataDelta = " +str(_dataDelta))
    
    mergeData(_data,_dataDelta)
    
    error.debug1(" data = " +str(_data))
    
    #executes all meta nodes, NOT IN PARALLEL
    keys = [] #gets around the 'can't change what you are itterating over' error
    for i in _nodeList.keys():
        keys.append(i)    
    for i in keys:
        if i in _nodeList.keys():
            if _nodeList[i].isMeta:
                pass
    
    #for controling how long to sleep
    _endTime = time.clock()
    time.sleep(max(0,stepDelay - (_endTime - _startTime)))
    

#-------------------------------------------------------------------------------
error.log("net finished execution")
error.log(" step = "+str(_step))
for i in _nodeList.keys():
    if _nodeList[i].isIO:
        _nodeList[i].close()
error.log(" I/O closed")

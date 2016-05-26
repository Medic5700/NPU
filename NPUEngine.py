class NPUEngine:
    import inspect
    import copy
    import functools
    import time
    import pickle
    
    def __init__(self, debugMode=False, debugLevel=0, logfile=None):
        #Higher debug level is more detailed [0,2] #0=regular logging, 1=program testing logging, 2=debug net while running
        self._VersionNumber = "v0.12"
        self.error = self.Debug(debugMode, debugLevel, logfile)
        self.error.log("Starting NPUEngine " + self._VersionNumber + " ==========================================")
        
        self._recursionDepth = 256 #the depth that recursive nodes will be parsed, only used for nodeList initialization
        #self._stepLimit = 256 #controls how many 'steps' a program can take at most
        #step limit should not be needed as it won't be executed as descrete steps like in the prototype NPU
        
        self.error.log("NPUEngine Initilized")
    
    def loadProgramFile(self, filename):
        """Allows you to load a program from a file"""
        pass
    
    ''' #API to be implemented later
    def loadProgramRawCode(self, code):
        """Allows you to load a program from a string"""
        pass
        
    def loadProgramModual(self, name):
        """Allows you to load a program from the same scope?"""
        pass
    
    def burstWrite(self, nodeName, dataList):
        """Writes a list worth of input to a specific input node"""
        pass
    
    def burstRead(self, nodeName):
        """Reads all pending output from a specific output node"""
        pass
    
    def readAll(self):
        """Reads all output from all output nodes, returns a dictionary"""
        pass
    
    def status(self):
        """Returns a string representing the status of the engine"""
        pass
    
    def save(self, filepath):
        """saves all neccassary parts of engine, including current state, to file. May impact performance"""
        #will use the pickle module
        pass
    
    def load(self, filepath):
        """loads a previously saved program net"""
        pass
    '''
    def read(self, nodeName):
        """Reads output from a specific output node"""
        pass
    
    def write(self, nodeName, data):
        """Writes input to a specific input node"""
        pass
    
    
    class Debug:
        """Class for logging and debuging"""
        import time
        
        def __init__(self, debugMode, level=0, file=None):
            self.__filename = file #set to None if you don't want a log file writen
            self.showDebug = debugMode #Bool
            self.level = level
            
        def __save(self, text):
            """Function to save each log entry"""
            if (self.__filename != None):
                logfile = open(self.__filename, 'a')
                try:
                    logfile.write(text)
                except:
                    self.error("Error Occured in Error Logging Function: Attempting to report previous error")
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
            temp = "[" + self.time.asctime() + "] Log: " + text
            print(temp)
            self.__save(temp + "\n")
        
        def error(self, text):
            """Takes string, pushes to stdout and saves it to the log file
            
            Mainly meant for non-recoverable errors that should cause the program to terminate"""
            temp = "[" + self.time.asctime() + "] ERROR: " + text
            print(temp)
            self.__save(temp + "\n")
            
        def warning(self, text):
            """Takes string, pushes to stdout and saves it to the log file
            
            Meant for non-program ending bugs and errors"""
            temp = "[" + self.time.asctime() + "] WARNING: " + text
            print(temp)
            self.__save(temp + "\n")          
        
        def debug(self, level, *args):
            """takes n number of strings, pushes to stdout and log file
            
            only writes input to stdout/log file when showDebug is True"""
            if (self.showDebug and (self.level >= level)):
                temp = "Debug" + str(level) + ":"
                for i in args:
                    temp += "\t" + str(i) + "\n"
                print(temp, end="") #fixes issue where log and sceen output newlines don't match
                self.__save(temp)

if (__name__ == "__main__"):
    #engine testing is done here
    engine1 = NPUEngine(True,2,"NPUEngine.log")

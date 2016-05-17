import baseNodes

class NPUEngine:
    import inspect
    import copy
    import functools
    import time
    
    def __init__(self, stepLimit=256, debugMode=False, debugLevel=0, logfile="NPUEngine.log"):
        #Higher debug level is more detailed [0,1]
        self._VersionNumber = "v0.12"
        self.error = self.Debug(debugMode, debugLevel, logfile)
        self.error.log("Starting NPUEngine " + self._VersionNumber + " ==========================================")
        
        self._recursionDepth = 256 #the depth that encapsulated nodes will be parsed, only used for nodeList initialization
        self._stepLimit = 256 #controls how many 'steps' a program can take at most
        
        self.error.log("NPUEngine Initilized")
    
    def loadProgramFile(self, filename):
        """Allows you to load a program from a file"""
        pass
    
    def loadProgramRawCode(self, code):
        """Allows you to load a program from a string"""
        pass
    
    def loadProgramModual(self, name):
        """Allows you to load a program from the same scope"""
        pass
    
    def write(self, nodeName, data):
        """Writes input to a specific input node"""
        pass
    
    def read(self, nodeName):
        """Reads output from a specific output node"""
        pass
    
    def readAll(self):
        """Reads all output from all output nodes, returns a dictionary"""
        pass
    
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
    engine1 = NPUEngine()

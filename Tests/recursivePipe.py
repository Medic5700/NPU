#generates net with 512 nodes (forming a line), passes input through nodes, kind of like a pipe
#tests engine recursion

class main():
    def __init__(self, depth=0):
        self.depth=depth
    def makeNet(self, classList):
        nodeList = {}
        table = {}
        if (self.depth == 0):
            nodeList["input"] = classList["input"]()
            nodeList["main"] = classList["main"](self.depth+1)
            nodeList["output"] = classList["output"]()
            table["main"] = {0:{"input":0}}
            talbe["output"] = {0:{"main":0}}
        elif (self.depth < 512):
            nodeList["main"] = classList["main"](self.depth+1)
            table["main"] = {0:{"in":0}}
            table["out"] = {0:{"Main":0}}
        else:
            table["out"] = {0:{"in":0}}
            
        return nodeList, table

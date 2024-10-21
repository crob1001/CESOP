import textwrap

__author__ = "Christian Roberts"

class xmlElement:

    def __init__(self, tag: str, nameSpace: str = None, child: any = None, inline: bool = False):

        self.attribDict = {}
        self.children = []

        self.tag = tag
        self.inline = inline
        self.nameSpace = nameSpace
        
        #if indented any further move to seperate funct
        if (None != child):
            match(type(child)):
                case tuple() | set() | list():
                    self.addChildren(child)

                case _:
                    self.children.append(child)

    def getNameSpace(self) -> str:
        return self.nameSpace

    def getAttribs(self) -> dict:
        return self.attribDict

    def getAttribValue(self, attrib: str) -> str:
        return self.attribDict.get(attrib)
    
    def getTag(self) -> str:
        return self.tag
    
    def addChild(self, child: any):
        self.children.append(child)
    
    def addChildren(self, children: list | tuple | set):
        for i in children: 
            self.children.append(i)

    def insertChild(self, child, loc: int):
        self.children.insert(loc, child)

    def updateAttrib(self, attrib: str, value = ""):
        self.attribDict[attrib] = f"\"{value}\""
    
    def setNameSpace(self, nameSpace: str):
        self.nameSpace = nameSpace

    def setTag(self, tag: str):
        self.tag = tag
    
    def setInline(self, inline: bool):
        self.inline = inline
    
    def __str__(self) -> str:
        
        if None != self.nameSpace:
            out = f"<{self.nameSpace}:{self.tag}"
        else:
            out = f"<{self.tag}"

        for i in self.attribDict:
            out = f"{out} {i}={self.attribDict[i]}"

        if (0 >= len(self.children)):
            out = f"{out}/>\n"
            return out
        
        #if this needs to be indented more split out into multiple functs
        if(False == self.inline):
            out = f"{out}>\n"
            for i in self.children:
                if (isinstance(i, xmlElement)):
                    out = out + textwrap.indent(i.__str__(), '\t')
                else:
                    out = out + textwrap.indent(str(i), '\t') + "\n"
        #if this needs to be indented more split out into multiple functs
        else:
            out = f"{out}>"
            for i in self.children:
                if (isinstance(i, xmlElement)):
                    i.setInline(True)
                    out = out + i.__str__().rstrip('\n')
                else:
                    out = out + str(i)

        if None != self.nameSpace:
            out = f"{out}</{self.nameSpace}:{self.tag}>\n"
        else:
            out = f"{out}</{self.tag}>\n"
        

        return out
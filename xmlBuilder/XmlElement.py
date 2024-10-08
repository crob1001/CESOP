import textwrap

__author__ = "Christian Roberts"

class XmlElement:

    def __init__(self, tag, child = None, inline = False):
        # moved into init to prevents attribs from being accessed by content when it's content is an xmlElement
        # no I don't know why it this was happening 
        self.attribDict = {}
        self.children = []

        self.tag = tag

        self.inline = inline
        
        if (None != child):
            self.children.append(child)

    def updateAttrib(self, attrib, value = ""):
        self.attribDict[attrib] = f"\"{value}\""

    #if this needs to be indented more slit out into multiple functs
    def __str__(self) -> str:
        out = f"<{self.tag}"
        for i in self.attribDict:
            out = f"{out} {i}={self.attribDict[i]}"
        if (0 >= len(self.children)):
            out = f"{out}/>\n"
        else:
            if(False == self.inline):
                out = f"{out}>\n"
                for i in self.children:
                    if (isinstance(i, XmlElement)):
                        out = out + textwrap.indent(i.__str__(), '\t')
                    else:
                        out = out + textwrap.indent(str(i), '\t') + "\n"
                out = out + "</"+self.tag+">\n"
            else:
                out = f"{out}>"
                for i in self.children:
                    if (isinstance(i, XmlElement)):
                        i.setInline(True)
                        out = out + i.__str__().rstrip('\n')
                    else:
                        out = out + str(i)
                out = out + "</"+self.tag+">\n"
        return out

    # def setcontent(self, content):
    #     self.content = content

    def addChild(self, child):
        self.children.append(child)
    
    def addChildren(self, children):
        for i in children: 
            self.children.append(i)

    def insertChild(self, child, loc):
        self.children.insert(loc, child)

    def getTag(self) -> str:
        return self.tag
    
    def setTag(self, tag):
        self.tag = tag

    def getAttribs(self) -> dict:
        return self.attribDict

    def getAttribValue(self, attrib) -> str:
        return self.attribDict.get(attrib)
    
    def setInline(self, inline):
        self.inline = inline
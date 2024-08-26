import sys
import datetime
from pathlib import Path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QAction, QLabel, QPushButton

import globals
import builder
import guiElements.SeperatingLine as SeperatingLine
import guiElements.LabeledTextBox as LabeledTextBox
import guiElements.LabeledComboBox as LabeledComboBox
import xmlBuilder.fileHandlerWidget as fileHandlerWidget

__author__ = "Christian Roberts"

# @dataclass
# class 

LOGO_PATH = Path(sys.argv[0]).parent.absolute().__str__()+'/assets/logo.png'
EXIT_ICON_PATH = Path(sys.argv[0]).parent.absolute().__str__()+'/assets/exit.png'

app = QApplication(sys.argv)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)

        self.setWindowIcon(QIcon(LOGO_PATH))
        self.setGeometry(100, 100, 450, 100)
        self.setWindowTitle("Cesop Report Builder GUI")

        self.initMenuBar()

        mainContainer = self.createContainer()
        self.setCentralWidget(mainContainer)

        self.quarterComboBox = LabeledComboBox.LabeledComboBox()
        self.quarterComboBox.setFields("Quarter:", globals.__quarters__.keys())

        self.CountryComboBox = LabeledComboBox.LabeledComboBox()
        self.CountryComboBox.setFields("Country Code:", globals.__countries__.keys())

        self.yearInputBox = LabeledTextBox.LabeledTextBox()
        self.yearInputBox.setFields("Year:", "YYYY", str(datetime.date.today().year))

        self.pspIDInputBox = LabeledTextBox.LabeledTextBox() 
        self.pspIDInputBox.setFields("pspID:", "pspID", globals.__pspID__)

        self.pageNumInputBox = LabeledTextBox.LabeledTextBox()
        self.pageNumInputBox.setFields("Page Num:", "1")

        self.pageTotalInputBox = LabeledTextBox.LabeledTextBox()
        self.pageTotalInputBox.setFields("Total Pages:", "1")


        self.MessageTypeIndic = LabeledComboBox.LabeledComboBox()
        self.MessageTypeIndic.setFields("Message Indic:", globals.__MsgTypeIndic__.keys())

        self.pspIdType = LabeledComboBox.LabeledComboBox()
        self.pspIdType.setFields("PSPIdType:", globals.__pspIDType__.keys())


        self.name = LabeledTextBox.LabeledTextBox(400)
        self.name.setFields("Company name:", "name", globals.__CompanyName__)

        self.nameType = LabeledComboBox.LabeledComboBox()
        self.nameType.setFields("Name Type:", globals.__NameTypes__.keys())

        
        self.fileHandler = fileHandlerWidget.fileHandlerWidget()

        
        mainContainer.layout().addWidget(SeperatingLine.SeperatingLine().getWidget(), 0, 0, 1, 6)

        mainContainer.layout().addWidget(self.quarterComboBox.getWidget(), 1, 0)
        mainContainer.layout().addWidget(self.CountryComboBox.getWidget(), 1, 1)
        mainContainer.layout().addWidget(self.yearInputBox.getWidget(), 1, 2)
        mainContainer.layout().addWidget(self.pspIDInputBox.getWidget(), 1, 3)
        mainContainer.layout().addWidget(self.pageNumInputBox.getWidget(), 1, 4)
        mainContainer.layout().addWidget(self.pageTotalInputBox.getWidget(), 1, 5)

        mainContainer.layout().addWidget(SeperatingLine.SeperatingLine().getWidget(), 2, 0, 1, 6)

        mainContainer.layout().addWidget(self.MessageTypeIndic.getWidget(), 3, 0)
        mainContainer.layout().addWidget(QLabel("CESOP100: The message contains new data.\n"+
                                                "CESOP101: The message contains corrections or deletions of previously sent data.\n"+
                                                "CESOP102: The message indicates there is no data to report."), 3, 1, 1,3)
        mainContainer.layout().addWidget(self.pspIdType.getWidget(), 3, 4)

        mainContainer.layout().addWidget(SeperatingLine.SeperatingLine().getWidget(), 4, 0, 1, 6)

        mainContainer.layout().addWidget(self.name.getWidget(), 5, 0, 1, 2)
        mainContainer.layout().addWidget(self.nameType.getWidget(), 5, 2)
        mainContainer.layout().addWidget(QLabel("LEGAL: Legal name                   TRADE: Trade name\n"+ 
                                                "BUSINESS: Business name        PERSON: Person name\n"+
                                                "OTHER: Other name"), 5, 3, 1,3)

        mainContainer.layout().addWidget(SeperatingLine.SeperatingLine().getWidget(), 6, 0, 1, 6)

        mainContainer.layout().addWidget(self.fileHandler.getWidget(), 7, 0, 1, 3)

        mainContainer.layout().addWidget(SeperatingLine.SeperatingLine().getWidget(), 8, 0, 1, 6)

        mainContainer.layout().addWidget(self.tempBtn(), 12, 5)

        # mainContainer.layout().addWidget(self.tempTempBtn(), 13, 5)

    def tempBtn(self):
        btn = QPushButton()
        btn.setText("Generate")
        btn.clicked.connect(self.build)
        return btn

    def build(self):
        builder.build(list(globals.__quarters__.keys())[self.quarterComboBox.getindex()], self.yearInputBox.getInputText(),
                    list(globals.__countries__.keys())[self.CountryComboBox.getindex()], self.pspIDInputBox.getInputText(), 
                    self.pageNumInputBox.getInputText(), self.pageTotalInputBox.getInputText(),
                    list(globals.__MsgTypeIndic__.keys())[self.MessageTypeIndic.getindex()],
                    list(globals.__pspIDType__.keys())[self.pspIdType.getindex()], self.name.getInputText(),
                    list(globals.__NameTypes__.keys())[self.nameType.getindex()], self.fileHandler.getFileList()
                    )

    def createContainer(self):
        container = QWidget(self)
        container.setLayout(QGridLayout())
        # container.setContentsMargins(5, 5, 5, 5)
        return container

    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        # exit menu item
        fileMenu.addSeparator()
        exitAction = QAction(QIcon(EXIT_ICON_PATH), '&Exit', self)
        exitAction.setStatusTip('Exit')
        exitAction.setShortcut('Alt+F4')
        exitAction.triggered.connect(self.quit)
        fileMenu.addAction(exitAction)

        abtMenu = menuBar.addMenu('&About')
        abtMenu.addAction(QAction("Software Version: "+globals.__version__, self))
        abtMenu.addAction(QAction("Software Version: "+globals.__cesopVersion__, self))

        # status bar
        self.status_bar = self.statusBar()
        self.show()

    def quit(self):
        # if self.confirm_save():
        self.destroy()
        app.quit()
        self.close()

def runGui():
    window = MainWindow()
    sys.exit(app.exec())
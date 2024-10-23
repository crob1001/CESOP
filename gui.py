import sys
import datetime
from pathlib import Path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QAction, QLabel, QPushButton

import globals
from reportBuilder import main
from guiElements import SeperatingLine, LabeledTextBox, LabeledComboBox, fileHandlerWidget

__author__ = "Christian Roberts"

LOGO_PATH = Path(sys.argv[0]).parent.absolute().__str__()+'/assets/logo.png'

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
        self.quarterComboBox.setFields("Quarter:", globals.__QUARTERS__.keys())

        self.countryComboBox = LabeledComboBox.LabeledComboBox()
        self.countryComboBox.setFields("Country Code:", globals.__COUNTRIES__.keys())

        self.yearInputBox = LabeledTextBox.LabeledTextBox()
        self.yearInputBox.setFields("Year:", "YYYY", str(datetime.date.today().year))

        self.pspIDInputBox = LabeledTextBox.LabeledTextBox() 
        self.pspIDInputBox.setFields("pspID:", "pspID", globals.__PSP_ID__)

        self.pageNumInputBox = LabeledTextBox.LabeledTextBox()
        self.pageNumInputBox.setFields("Page Num:", "1")

        self.pageTotalInputBox = LabeledTextBox.LabeledTextBox()
        self.pageTotalInputBox.setFields("Total Pages:", "1")


        self.messageTypeIndic = LabeledComboBox.LabeledComboBox()
        self.messageTypeIndic.setFields("Message Indic:", globals.__MSG_TYPE_INDIC__.keys())

        self.pspIdType = LabeledComboBox.LabeledComboBox()
        self.pspIdType.setFields("PSP Id Type:", globals.__PSP_ID_TYPE__.keys())


        self.name = LabeledTextBox.LabeledTextBox(400)
        self.name.setFields("Sending PSP Name:", "name", globals.__SENDING_PSP_NAME__)

        self.nameType = LabeledComboBox.LabeledComboBox()
        self.nameType.setFields("Name Type:", globals.__NAME_TYPES__.keys())

        
        self.fileHandler = fileHandlerWidget.fileHandlerWidget()

        
        mainContainer.layout().addWidget(SeperatingLine.SeperatingLine().getWidget(), 0, 0, 1, 6)

        mainContainer.layout().addWidget(self.quarterComboBox.getWidget(), 1, 0)
        mainContainer.layout().addWidget(self.countryComboBox.getWidget(), 1, 1)
        mainContainer.layout().addWidget(self.yearInputBox.getWidget(), 1, 2)
        mainContainer.layout().addWidget(self.pspIDInputBox.getWidget(), 1, 3)
        mainContainer.layout().addWidget(self.pageNumInputBox.getWidget(), 1, 4)
        mainContainer.layout().addWidget(self.pageTotalInputBox.getWidget(), 1, 5)

        mainContainer.layout().addWidget(SeperatingLine.SeperatingLine().getWidget(), 2, 0, 1, 6)

        mainContainer.layout().addWidget(self.messageTypeIndic.getWidget(), 3, 0)
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

    def tempBtn(self):
        btn = QPushButton()
        btn.setText("Generate")
        btn.clicked.connect(self.build)
        return btn

    def build(self):
        main.main(list(globals.__QUARTERS__.keys())[self.quarterComboBox.getindex()], self.yearInputBox.getInputText(),
                    list(globals.__COUNTRIES__.keys())[self.countryComboBox.getindex()], self.pspIDInputBox.getInputText(), 
                    self.pageNumInputBox.getInputText(), self.pageTotalInputBox.getInputText(),
                    list(globals.__MSG_TYPE_INDIC__.keys())[self.messageTypeIndic.getindex()],
                    list(globals.__PSP_ID_TYPE__.keys())[self.pspIdType.getindex()], self.name.getInputText(),
                    list(globals.__NAME_TYPES__.keys())[self.nameType.getindex()], self.fileHandler.getFileList()
                    )

    def createContainer(self):

        container = QWidget(self)
        container.setLayout(QGridLayout())

        return container

    def initMenuBar(self):

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')

        fileMenu.addSeparator()
        exitAction = QAction(QIcon(), '&Exit', self)
        exitAction.setStatusTip('Exit')
        exitAction.setShortcut('Alt+F4')
        exitAction.triggered.connect(self.quit)
        fileMenu.addAction(exitAction)

        abtMenu = menuBar.addMenu('&About')
        abtMenu.addAction(QAction("Software Version: " + globals.__VERSION__, self))
        abtMenu.addAction(QAction("Software Version: " + globals.__CESOP_VERSION__, self))

        # status bar
        self.status_bar = self.statusBar()
        self.show()

    def quit(self):

        self.destroy()
        app.quit()
        self.close()

def runGui():
    window = MainWindow()
    sys.exit(app.exec())
from PyQt5.QtWidgets import QFileDialog, QWidget, QGridLayout, QPushButton, QListWidget

__author__ = "Christian Roberts"

class fileHandlerWidget:

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.addFile = QPushButton()
        self.addFile.setText("Add")
        self.addFile.clicked.connect(self.addItem)
        self.removeFile = QPushButton()
        self.removeFile.setText("Remove")
        self.removeFile.clicked.connect(self.removeItem)
        self.fileList = QListWidget()
        self.container = QWidget()


        self.container.setLayout(QGridLayout())

        self.container.layout().addWidget(self.addFile, 0, 0, 1, 1)
        self.container.layout().addWidget(self.removeFile, 1, 0, 1, 1)
        self.container.layout().addWidget(self.fileList, 0, 1, 2, 1)

    def addItem(self):
        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            self.fileList.addItem(filename)

    def removeItem(self):
        for item in self.fileList.selectedItems():
            self.fileList.takeItem(self.fileList.row(item))
        
    def getWidget(self):
        return self.container
    
    def getFileList(self):
        return [self.fileList.item(x).text() for x in range(self.fileList.count())]
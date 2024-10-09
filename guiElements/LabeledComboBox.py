from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox

__author__ = "Christian Roberts"

class LabeledComboBox:

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.index = 0
        self.label = QLabel()
        self.combo = QComboBox()
        self.container = QWidget()

        self.container.setLayout(QGridLayout())
        self.container.setMaximumSize(200, 50)

        self.container.layout().addWidget(self.label, 0, 0)
        self.container.layout().addWidget(self.combo, 0, 1)

        self.label.setAlignment(Qt.AlignRight | Qt.AlignCenter)

    def setFields(self, labelText, selectionList):
        
        self.label.setText(labelText)

        self.combo.addItems(selectionList)
        
        self.combo.currentIndexChanged.connect(self.setIndex)

    def setIndex(self, i):
        self.index = i
        
    def getWidget(self):
        return self.container
    
    def getindex(self):
        return self.index
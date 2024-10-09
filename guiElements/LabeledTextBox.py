from PyQt5.QtWidgets import QTextEdit, QWidget, QGridLayout, QLabel

__author__ = "Christian Roberts"

class LabeledTextBox:

    def __init__(self, maxsize = 200):

        super().__init__()

        self.default = ""

        self.label = QLabel()
        self.textField = QTextEdit()
        self.container = QWidget()

        # container = QWidget(self)
        self.container.setLayout(QGridLayout())
        self.container.setMaximumSize(maxsize, 50)

        self.container.layout().addWidget(self.label, 0, 0)
        self.container.layout().addWidget(self.textField, 0, 1)

    def setFields(self, labelText = "", placeholder = "", text = ""):
        self.label.setText(labelText)

        self.textField.setPlaceholderText(placeholder)

        self.default = placeholder

        self.textField.setText(text)
        
    def getWidget(self):
        return self.container
    
    def getInputText(self):

        if (self.textField.toPlainText() != ""):
            return self.textField.toPlainText()
        else:
            return self.default
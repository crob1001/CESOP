import globals
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

__author__ = "Christian Roberts"

def exitAction(self):
        exitAction = QAction(QIcon(), '&Exit', self)
        exitAction.setStatusTip('Exit')
        exitAction.setShortcut('Alt+F4')
        exitAction.triggered.connect(self.quit)

        return exitAction

def createToggleAction(self, itemName: str, funct):
        action = QAction('Include ' + itemName, self, checkable=True)
        action.setStatusTip('Include ' + itemName)
        action.setChecked(globals.__OPTIONAL__[itemName.upper()])
        action.triggered.connect(funct)

        return action
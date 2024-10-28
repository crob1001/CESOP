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

# def toggleVatId(self):
#         action = QAction('Include VatId', self, checkable=True)
#         action.setStatusTip('Include VatId')
#         action.setChecked(globals.__OPTIONAL__["VATID"])
#         action.triggered.connect(toggle.toggleVat)

#         return action

# def toggleTaxId(self):
#         action = QAction('Include TaXId', self, checkable=True)
#         action.setStatusTip('Include TaXId')
#         action.setChecked(globals.__OPTIONAL__["TAXID"])
#         action.triggered.connect(toggle.toggleTax)

#         return action

# def toggleAddressFix(self):
#         action = QAction('Include Address_Fix', self, checkable=True)
#         action.setStatusTip('Include Address_Fix')
#         action.setChecked(globals.__OPTIONAL__["ADDRESS_FIX"])
#         action.triggered.connect(toggle.toggleAddressFix)

#         return action

# def toggleAddressFree(self):
        
#         action = QAction('Include Address_Free', self, checkable=True)
#         action.setStatusTip('Include Address_Free')
#         action.setChecked(globals.__OPTIONAL__["ADDRESS_FREE"])
#         action.triggered.connect(toggle.toggleAddressFree)

#         return action
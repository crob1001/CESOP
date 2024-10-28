from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame

__author__ = "Christian Roberts"

class SeperatingLine:

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.separador = QFrame()
        self.container = QWidget()

        self.separador.setFrameShape(QFrame.HLine)
        self.separador.setLineWidth(1)
        self.container.setLayout(QGridLayout())
        self.container.layout().addWidget(self.separador, 0, 0)

    def getWidget(self):
        return self.container
    
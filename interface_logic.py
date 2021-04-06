import os

import numpy as np

from interface import Ui_MainWindow
from PyQt5 import QtWidgets, uic, Qt, QtCore
import sys


# import variables


class Interface(QtWidgets.QMainWindow):
    genomeLayout: QtWidgets.QVBoxLayout

    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        # print(self.PauseButton)
        # self.PauseButton.clicked.connect(self.stop_game)
        self.move((1920 - self.width()) // 2 + 640, (1080 - self.height() - 75) // 2)
        self.pushButton.clicked.connect(self.stop_game)
        self.genomeLayoutList = []
        for i in range(8):
            horizontal_layout = QtWidgets.QHBoxLayout()
            self.genomeLayoutList.append([])
            for j in range(8):
                qlabel = QtWidgets.QLabel()
                self.genomeLayoutList[i].append(qlabel)
                qlabel.setAlignment(QtCore.Qt.AlignCenter)
                # qlabel.setText(str(0))
                horizontal_layout.addWidget(qlabel)
            self.genomeLayout.addLayout(horizontal_layout)

    def fill_genome_field(self, sprite):
        genome = sprite.genome.copy()
        genome.resize(8, 8)

        for i in range(self.genomeLayout.count()):
            for j in range(self.genomeLayout.itemAt(i).count()):
                self.genomeLayoutList[i][j].setText(str(genome[i][j]))
                # self.genomeLayoutList[i][j].setText(str(genome[i][j]))
                # self.genomeLayout.itemAt(i).itemAt(j).setText(str(genome[i][j]))

        # genome = sprite.genome
        # for i in range(8):
        #     self.
        #     for j in range(8):

    @staticmethod
    def stop_game():
        from variables import stop_lock
        import variables
        with stop_lock:
            variables.stop = not variables.stop

    def closeEvent(self, event):
        os._exit(1)
        event.acept()


app = QtWidgets.QApplication(sys.argv)
window = Interface()


def run_interface():
    window.show()
    app.exec_()

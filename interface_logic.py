import os
import sys

from PyQt5 import QtWidgets, uic, QtCore


# import variables


class Interface(QtWidgets.QMainWindow):
    genomeLayout: QtWidgets.QVBoxLayout

    def __init__(self, pipe):
        super().__init__()
        uic.loadUi("interface.ui", self)
        self.move((1920 - self.width()) // 2 + 640, (1080 - self.height() - 75) // 2)
        self.stopButton.clicked.connect(self.stop_game)
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
        self.pipe = pipe

    def fill_window(self, sprite):
        self.fill_genome_field(sprite)
        self.fill_energy_labels(sprite)

    def clear_window(self):
        self.clear_genome_field()
        self.clear_labels()

    def fill_energy_labels(self, sprite):
        self.eaten_cells_label.setText("Клеток съедено: " + str(sprite.from_cells_energy_counter))
        self.sun_count_label.setText("Солнца поглащено: " + str(sprite.from_sun_energy_counter))
        self.minerals_count_label.setText("Минералов поглащено: " +
                                          str(sprite.from_minerals_energy_counter))

    def fill_genome_field(self, sprite):
        genome = sprite.genome.copy()
        genome.resize(8, 8)

        for i in range(self.genomeLayout.count()):
            for j in range(self.genomeLayout.itemAt(i).count()):
                self.genomeLayoutList[i][j].setText(str(genome[i][j]))

    def clear_genome_field(self):
        for i in range(self.genomeLayout.count()):
            for j in range(self.genomeLayout.itemAt(i).count()):
                self.genomeLayoutList[i][j].setText("")

    def clear_labels(self):
        self.eaten_cells_label.setText("")
        self.sun_count_label.setText("")
        self.minerals_count_label.setText("")

    def stop_game(self):
        self.pipe.send(("toggle_pause",))

    def fill_cells_count(self, game):
        self.cells_count_on_field.setText("Количество клеток на поле: " + str(len(
            game.cells_group)))

    def closeEvent(self, event):
        os._exit(1)
        event.acept()





def run_interface(pipe):
    app = QtWidgets.QApplication(sys.argv)
    window = Interface(pipe)
    window.show()
    app.exec_()

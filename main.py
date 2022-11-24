import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super(Coffee, self).__init__()

        self.pod = sqlite3.connect('coffee.sqlite3')
        self.cu = self.pod.cursor()
        self.great()

    def great(self):
        uic.loadUi('main.ui', self)
        data = self.cu.execute("select * from coffee").fetchall()
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                t = QTableWidgetItem(str(elem))
                self.tableWidget.setItem(
                    i, j, t)

        self.pushButton.clicked.connect(self.run)

    def run(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.running)
        self.pushButton_2.clicked.connect(self.great)

    def running(self):
        n = self.comboBox.currentText()
        name = self.lineEdit_2.text()
        hot = self.lineEdit_3.text()
        grain = self.lineEdit_4.text()
        taste = self.lineEdit_5.text()
        free = str(self.spinBox.value())
        volume = str(self.spinBox_2.value())

        if 'Р' in n:
            m = "update coffee "
            r = "set "
            if hot:
                r = r + f"degree = '{hot}',"
            if grain:
                r = r + f" grinding = '{grain}',"
            if taste:
                r = r + f" taste = '{taste}',"
            if free:
                r = r + f" price = '{free}',"
            if volume:
                r = r + f"volume = '{volume}'"
            p = f" where nameSort = '{name}'"
            nn = m + r + p
            self.cu.execute(nn).fetchall()
            self.pod.commit()

        else:
            m = f"insert into coffee(nameSort, degree, grinding, taste, "
            p = f"price, volume) values('{name}', '{hot}', '{grain}', '{taste}', '{free}', '{volume}')"
            mp = m + p
            self.cu.execute(mp).fetchall()
            self.pod.commit()

        self.great()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    co = Coffee()
    co.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

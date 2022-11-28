import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        uic.loadUi('main.ui', self)
        self.comboBox.addItem('Сорта кофе')
        self.comboBox.addItems([elem[0] for elem in self.cur.execute("""SELECT variety_name FROM coffee""").fetchall()])
        self.pushButton.setText('Показать информацию')
        self.pushButton.clicked.connect(self.saw_information)

    def saw_information(self):
        self.listWidget.clear()
        variety_name = self.comboBox.currentText()
        if variety_name == 'Сорта кофе':
            return
        else:
            roast_degree = [elem[0] for elem in self.cur.execute("""SELECT roast_degree FROM coffee
                            WHERE variety_name = """ + "'" + variety_name + "'").fetchall()][0]
            ground_inbeans = [elem[0] for elem in self.cur.execute("""SELECT ground_inbeans FROM coffee
                              WHERE variety_name = """ + "'" + variety_name + "'").fetchall()][0]
            taste_description = [elem[0] for elem in self.cur.execute("""SELECT taste_description FROM coffee
                                 WHERE variety_name = """ + "'" + variety_name + "'").fetchall()][0]
            price_rub = [elem[0] for elem in self.cur.execute("""SELECT price_rub FROM coffee
                         WHERE variety_name = """ + "'" + variety_name + "'").fetchall()][0]
            package_volume = [elem[0] for elem in self.cur.execute("""SELECT package_volume_gramms FROM coffee
                              WHERE variety_name = """ + "'" + variety_name + "'").fetchall()][0]
            self.listWidget.addItem('Сорт: ' + variety_name)
            self.listWidget.addItem('Прожарка: ' + roast_degree)
            self.listWidget.addItem('Молотый/в зернах: ' + ground_inbeans)
            self.listWidget.addItem('Описание вкуса: ' + taste_description)
            self.listWidget.addItem('Цена в рублях: ' + str(price_rub))
            self.listWidget.addItem('Обьем упаковки в граммах: ' + str(package_volume))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

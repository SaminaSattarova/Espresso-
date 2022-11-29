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
        self.pushButton_2.setText('Добавить/изменить')
        self.pushButton_2.clicked.connect(self.add_edit)
        self.pushButton_3.setText('Обновить список сортов')
        self.pushButton_3.clicked.connect(self.obn)

    def obn(self):
        self.comboBox.clear()
        self.comboBox.addItem('Сорта кофе')
        self.comboBox.addItems([elem[0] for elem in self.cur.execute("""SELECT variety_name FROM coffee""").fetchall()])

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

    def add_edit(self):
        self.addedit = AddEdit(self)
        self.addedit.show()


class AddEdit(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.pushButton.setText('Добавить')
        self.label.setText('Сорт: ')
        self.label_2.setText('Прожарка: ')
        self.label_3.setText('Молотый/в зернах: ')
        self.label_4.setText('Описание вкуса: ')
        self.label_5.setText('Цена в рублях: ')
        self.label_6.setText('Обьем упаковки: ')
        self.pushButton.clicked.connect(self.add)

    def add(self):
        a1 = self.lineEdit.text()
        a2 = self.lineEdit_2.text()
        a3 = self.lineEdit_3.text()
        a4 = self.lineEdit_4.text()
        a5 = self.lineEdit_5.text()
        a6 = self.lineEdit_6.text()
        self.cur.execute("""INSERT INTO coffee(variety_name, roast_degree, ground_inbeans, taste_description,
                                                price_rub, package_volume_gramms)
                            VALUES(?, ?, ?, ?, ?, ?);""", (a1, a2, a3, a4, a5, a6,))
        self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

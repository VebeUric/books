import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem


class BooksOrange(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.comboBox.addItem('Автор')
        self.comboBox.addItem('Название')
        connection = sqlite3.connect('book')
        self.cur = connection.cursor()
        self.criterion_dict = {
            'Автор': 'author',
            'Название': 'name'
        }
        self.information_window = InformationWindow()
        self.information_window.hide()
        self.pushButton.clicked.connect(self.search_book)

    def search_book(self):
        try:
            criterion = self.comboBox.currentText()
            word_part = self.lineEdit.text()
            result = self.get_book_list(word_part, criterion)
            self.list_widget_filler(result)
        except Exception as e:
            print(e, 6)

    def get_book_list(self, word_part, criterion):
        print(self.criterion_dict[criterion])
        print('ok')

        query = f"""
        SELECT * FROM books
        WHERE {self.criterion_dict[criterion]} LIKE ?
        """
        print(query)
        result = self.cur.execute(query, ('%' + word_part + '%',)).fetchall()
        print(result, 1)
        return result

    def get_solely_book(self, name):
        query = """
        SELECT * FROM books 
        WHERE name = ?
        """
        result = self.cur.execute(query, (name,)).fetchone()
        return result

    def list_widget_filler(self, book_list):
        try:
            self.listWidget.clear()
            for i in book_list:
                item = QListWidgetItem(i[1])
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.show_book_information)
        except Exception as e:
            print(e)

    def show_book_information(self, item):
        try:
            name = item.text()
            self.information_window.book = self.get_solely_book(name)
            self.information_window.show_book_information()
            self.information_window.show()
        except Exception as e:
            print(e)


class InformationWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('information.ui', self)

    def show_book_information(self):
        try:
            pixmap = QPixmap(f'book_photos/{self.book[5]}')
            self.photo.setPixmap(pixmap)
            self.name.setText(self.book[1])
            self.genre.setText(self.book[2])
            print(1)
            self.author.setText(self.book[4])
            self.year.setText(str(self.book[3]))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BooksOrange()
    ex.show()
    sys.exit(app.exec_())

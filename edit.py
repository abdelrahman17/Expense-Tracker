from UtilitiesMod import *
from editwindow import *
from categories import Categories
from Transactions import Transactions
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import QDate
import re
from datetime import date
from sys import exit
from pprint import pprint


class EditWindow(QDialog):
    def __init__(self, entry: dict, mainwindow):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()
        self.ui.back_pushButton.clicked.connect(self.close)
        self.ui.back_pushButton_2.clicked.connect(self.edit)
        self.entry = entry
        self.mainwindow = mainwindow
        self.categories = Categories().category_list[self.entry['type']]
        self.transactions = Transactions()
        self.load_entry()

    def load_entry(self):
        self.ui.type_label.setText(self.entry['type'])
        self.ui.amountlineEdit.setText(self.entry['amount'])
        date_ = [int(part) for part in self.entry['date'].split('-')]
        self.ui.dateEdit.setDate(QDate(date_[0], date_[1], date_[2]))
        self.ui.noteLineEdit.setText(self.entry['note'])
        self.ui.categories_combobox.clear()
        self.ui.categories_combobox.addItems(self.categories)
        self.ui.categories_combobox.setCurrentIndex(self.categories.index(self.entry['category']))

    def change(self):
        ui_date =[int(part) for part in self.ui.dateEdit.text().split('/')]
        ui_date = date(ui_date[2], ui_date[1], ui_date[0])
        entry_date = [int(part) for part in self.entry['date'].split('-')]
        entry_date = date(entry_date[0], entry_date[1], entry_date[2])

        ui_amount = float(self.ui.amountlineEdit.text())
        entry_amount = float(self.entry['amount'])

        ui_category = self.ui.categories_combobox.currentText()
        entry_category = self.entry['category']

        ui_note = self.ui.noteLineEdit.text().strip()
        entry_note = self.entry['note'].strip()

        return not (ui_amount == entry_amount and ui_category == entry_category and ui_note == entry_note and\
               ui_date == entry_date)

    def edit(self):
        if self.change():
            row_id = self.entry['row_id']
            category = self.ui.categories_combobox.currentText()
            amount = float(self.ui.amountlineEdit.text().strip())
            note = self.ui.noteLineEdit.text().strip()
            ui_date = [int(part) for part in self.ui.dateEdit.text().split('/')]
            ui_date = date(ui_date[2], ui_date[1], ui_date[0])
            self.transactions.edit(row_id, category, amount, ui_date, note)
            print('updated')
            self.transactions.refresh()
            self.mainwindow.load_table()


            self.entry['category'] = category
            self.entry['amount'] = amount
            self.entry['date'] = str(ui_date)
            self.entry['note'] = note


        else:
            print('nothing is edited to update')


if __name__ == '__main__':
    convert_ui('editwindow.ui')
    # app = QApplication([])
    # window = EditWindow(dict())
    # exit(app.exec_())

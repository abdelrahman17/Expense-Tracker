from UtilitiesMod import *
from addwindow import *
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QDate
from sys import argv, exit
from datetime import date
from categories import Categories
from Transactions import Transactions


class AddWindow(QDialog):
    def __init__(self, mainwindow):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.mainwindow = mainwindow
        self.ui.expense_radioButton.setChecked(True)
        self.ui.back_pushButton.clicked.connect(self.close)
        self.ui.savecategory_pushButton.clicked.connect(self.save_category)
        self.ui.income_radioButton.clicked.connect(self.refresh_categories)
        self.ui.expense_radioButton.clicked.connect(self.refresh_categories)
        self.category_manager = Categories()
        self.refresh_categories()

        ####################################
        # categories tab part
        ####################################
        self.ui.t_expense_radioButton.setChecked(True)
        self.ui.t_expense_radioButton.clicked.connect(self.refresh_transaction_categories)
        self.ui.t_income_radioButton.clicked.connect(self.refresh_transaction_categories)
        self.ui.t_dateEdit.setDate(QDate(date.today().year, date.today().month, date.today().day))
        self.ui.t_savebutton.clicked.connect(self.save_transaction)
        self.transaction_manager = Transactions()
        self.refresh_transaction_categories()

    def get_active_category(self):
        if self.ui.income_radioButton.isChecked():
            return 'income'
        else:
            return 'expense'

    def save_category(self):
        if self.ui.expense_radioButton.isChecked():
            category = 'expense'
        else:
            category = 'income'
        if self.ui.category_lineEdit.text() != "":
            if self.category_manager.save_category(category, self.ui.category_lineEdit.text()):
                QMessageBox.question(self,
                                     f'{category} Saved',
                                     f'{self.ui.category_lineEdit.text()} is added to {category}s successfully',
                                     QMessageBox.Ok)
                self.ui.category_lineEdit.clear()
                self.refresh_categories()
                self.refresh_transaction_categories()

            else:
                QMessageBox.question(self,
                                     'Category not added',
                                     f'{self.ui.category_lineEdit.text()} already exists',
                                     QMessageBox.Ok)
        else:
            QMessageBox.warning(self,
                                'No data input',
                                'Please enter the category name you wish to add first!',
                                QMessageBox.Ok)

    def refresh_categories(self):
        self.ui.categories_listWidget.clear()
        self.ui.categories_listWidget.addItems(self.category_manager.category_list[self.get_active_category()])

    ####################################
    # transaction tab part
    ####################################
    def get_active_transaction_category(self):
        if self.ui.t_expense_radioButton.isChecked():
            return 'expense'
        else:
            return 'income'

    def refresh_transaction_categories(self):
        self.ui.t_categories_combobox.clear()
        self.ui.t_categories_combobox.addItems(self.category_manager.category_list[self.get_active_transaction_category()])

    def save_transaction(self):
        if self.ui.t_categories_combobox.count() > 0 and self.ui.t_amountlineEdit.text() != "":
            category_type = self.get_active_transaction_category()
            category = self.ui.t_categories_combobox.currentText()
            amount = self.ui.t_amountlineEdit.text()
            date_ = self.ui.t_dateEdit.date().toPyDate()
            note = self.ui.t_notelineEdit.text()
            self.transaction_manager.add(category, amount, date_, note, category_type)
            QMessageBox.information(self,
                                    'Transaction Saved',
                                    f"{category.capitalize()} transaction is saved successfully.",
                                    QMessageBox.Ok)
            self.ui.t_amountlineEdit.clear()
            self.ui.t_notelineEdit.clear()
            self.transaction_manager.refresh()
            self.mainwindow.load_table()

        else:
            QMessageBox.warning(self,
                                'Missing Data',
                                'Please enter all the required data',
                                QMessageBox.Ok)


if __name__ == '__main__':
    convert_ui('addwindow.ui')


from UtilitiesMod import *
from Transactions import Transactions
from mainwindow import *
from edit import EditWindow
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from add import AddWindow
from sys import argv, exit
from pprint import pprint


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.transactions = Transactions()
        self.expenses = self.transactions.expense_transactions
        self.income = self.transactions.income_transactions
        self.ui.expense_radioButton.setChecked(True)
        self.load_table()
        self.show()
        self.ui.add_pushButton.clicked.connect(self.show_add_form)
        self.ui.tableWidget.cellPressed.connect(self.get_table_selection)
        self.ui.edit_pushButton.clicked.connect(self.edit_button_clicked)
        self.ui.income_radioButton.toggled.connect(self.income_radiobtn_clicked)
        self.ui.expense_radioButton.toggled.connect(self.expense_radiobtn_clicked)
        self.ui.delete_pushButton.clicked.connect(self.delete_button_clicked)

    def show_add_form(self):
        add_form = AddWindow(self)
        add_form.exec_()

    def load_table(self):
        self.ui.tableWidget.clearContents()
        if self.ui.income_radioButton.isChecked():
            dataframe = self.transactions.income_transactions
        else:
            dataframe = self.transactions.expense_transactions
        r, c = dataframe.shape
        self.ui.tableWidget.setRowCount(r)
        self.ui.tableWidget.setColumnCount(c + 1)
        row_count = 0
        for row_index, row_data in dataframe.iterrows():
            self.ui.tableWidget.setItem(row_count, 0, QTableWidgetItem(str(row_index)))
            self.ui.tableWidget.setItem(row_count, 1, QTableWidgetItem(row_data['category']))
            self.ui.tableWidget.setItem(row_count, 2, QTableWidgetItem(str(row_data['amount'])))
            self.ui.tableWidget.setItem(row_count, 3, QTableWidgetItem(row_data['date']))
            self.ui.tableWidget.setItem(row_count, 4, QTableWidgetItem(row_data['note']))
            self.ui.tableWidget.setItem(row_count, 5, QTableWidgetItem(row_data['type']))
            row_count += 1
        self.ui.tableWidget.setHorizontalHeaderLabels(['#', 'Category', 'Amount', 'Date', 'Memo','Type'])
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def get_table_selection(self):
        items = [item.text() for item in self.ui.tableWidget.selectedItems()]
        if items:
            selected_items = {'row_id': items[0],
                              'category': items[1],
                              'amount': items[2],
                              'date': items[3],
                              'note': items[4],
                              'type': items[5],
                              }
            return selected_items
        else:
            return False

    def edit_button_clicked(self):
        items = self.get_table_selection()
        pprint(items)
        if items:
            edit_dialog = EditWindow(items, self)
            edit_dialog.exec_()
            self.load_table()

        else:
            QMessageBox.question(self,
                                 'Nothing is selected',
                                 'Please select something first so you can edit it',
                                 QMessageBox.Ok)

    def income_radiobtn_clicked(self):
        if self.ui.income_radioButton.isChecked():
            self.load_table()

    def expense_radiobtn_clicked(self):
        if self.ui.expense_radioButton.isChecked():
            self.load_table()

    def delete_button_clicked(self):
        items = self.get_table_selection()
        if items:
            delete_question = QMessageBox.question(self,
                                                  'Delete Transaction',
                                                  'Are you sure you want to delete the selected transaction',
                                                   QMessageBox.Yes | QMessageBox.No)
            if delete_question == QMessageBox.Yes:
                self.transactions.delete(items['row_id'])
                self.load_table()
        else:
            QMessageBox.question(self,
                                 'Nothing is selected',
                                 'Please select something first so you can delete it',
                                 QMessageBox.Ok)



if __name__ == '__main__':
    convert_ui('mainwindow.ui')
    create_database()
    app = QApplication(argv)
    window = MainWindow()
    exit(app.exec_())

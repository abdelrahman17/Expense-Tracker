from UtilitiesMod import *
from Transactions import Transactions
from mainwindow import *
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
        self.show()
        self.ui.add_pushButton.clicked.connect(self.show_add_form)
        self.ui.tableWidget.cellPressed.connect(self.get_table_selection)

    def show_add_form(self):
        add_form = AddWindow()
        add_form.exec_()

    def load_table(self, type_):
        self.ui.tableWidget.clearContents()
        if type == 'income':
            dataframe = self.income
        else:
            dataframe = self.expenses
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
        selected_items = {'row_id': items[0],
                          'category': items[1],
                          'amount': items[2],
                          'date': items[3],
                          'note': items[4],
                          'type': items[5],
                          }
        print(selected_items)




if __name__ == '__main__':
    convert_ui('mainwindow.ui')
    create_database()
    app = QApplication(argv)
    window = MainWindow()
    window.load_table('expense')
    exit(app.exec_())

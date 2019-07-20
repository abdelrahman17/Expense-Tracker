from UtilitiesMod import convert_ui
from Transactions import *
from table import *
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.tran = Transactions()
        self.load_table(self.tran.expense_transactions)
        self.show()

    def load_table(self, dataframe):
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


if __name__ == '__main__':
    convert_ui('table.ui')
    app = QApplication([])
    window = Window()
    exit(app.exec_())


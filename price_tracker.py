from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
import sys
import requests
func = __import__("func")


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.rowCount = 1
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle("Flipcart Price Tracker")
        self.setGeometry(200, 40, 800, 680)
        self.setWindowIcon(QtGui.QIcon("C:/Users/Shawn James/Desktop/Python Projects/Amazon Prices/price_tracker.ico"))

        self.header = QLabel("PRICE TRACKER")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setFont(QtGui.QFont("family", 20))
        self.header.setStyleSheet("color:brown")

        self.lineedit = QLineEdit(self)
        self.lineedit.setGeometry(0, 0, 500, 30)
        self.lineedit.setMinimumSize(300, 30)
        self.lineedit.setPlaceholderText("Enter product address")
        self.lineedit.returnPressed.connect(lambda:self.addProduct(self.lineedit.text()))

        self.button = QPushButton("")
        self.button.setIcon(QtGui.QIcon("C:/Users/Shawn James/Desktop/Python Projects/Amazon Prices/Oxygen-Icons.org-Oxygen-Actions-dialog-ok-apply.ico"))
        self.button.clicked.connect(lambda:self.addProduct(self.lineedit.text()))

        self.table = QTableWidget()
        self.table.setRowCount(self.rowCount)
        self.table.setColumnCount(2)
        self.table.horizontalHeader().setSectionResizeMode(1)

        product_title = QTableWidgetItem("Product")
        product_title.setTextAlignment(QtCore.Qt.AlignCenter)
        product_title.setFont(QtGui.QFont("family", 14, QtGui.QFont.Bold))
        self.table.setItem(0, 0, product_title)

        price_title = QTableWidgetItem("Price")
        price_title.setTextAlignment(QtCore.Qt.AlignCenter)
        price_title.setFont(QtGui.QFont("family", 14, QtGui.QFont.Bold))
        self.table.setItem(0, 1, price_title)

        self.addInitialProducts()

        self.vbox = QVBoxLayout()
        self.vbox.stretch(1)
        hbox = QHBoxLayout()
        hbox.addWidget(self.lineedit)
        hbox.addWidget(self.button)
        self.vbox.addWidget(self.header)
        self.vbox.addLayout(hbox)
        self.vbox.addWidget(self.table)

        self.setLayout(self.vbox)
        self.show()

    def addProduct(self, link):
        details = func.get_product_price(link)
        product_name = details[0]
        product_price = details[1].lstrip("₹")

        warning = QMessageBox()
        warning.setWindowTitle("Error")
        warning.setIcon(QMessageBox.Warning)

        if details == "Invalid URL":
            warning.setText("The URL you entered is invalid!")
            x = warning.exec_()
        elif details == "No Connection":
            warning.setText("Check your network connection")
            x = warning.exec_()
        else:
            with open("links.txt", 'a') as links_file:
                links_file.write(link+"\n")

            self.rowCount += 1
            self.table.setRowCount(self.rowCount)

            product = QTableWidgetItem(product_name)
            product.setTextAlignment(QtCore.Qt.AlignCenter)
            product.setFont(QtGui.QFont("family", 14))
            self.table.setItem(self.rowCount-1, 0, product)

            price = QTableWidgetItem(product_price)
            price.setTextAlignment(QtCore.Qt.AlignCenter)
            price.setFont(QtGui.QFont("family", 13))
            self.table.setItem(self.rowCount-1, 1, price)

    def addInitialProducts(self):
        try:
            requests.get("http://www.google.com")
        except requests.exceptions.ConnectionError:
            warning = QMessageBox()
            warning.setWindowTitle("Error")
            warning.setIcon(QMessageBox.Warning)
            warning.setText("Check your network connection")
            x = warning.exec_()
            sys.exit()
        else:
            with open("links.txt") as links_file:
                for link in links_file:
                    details = func.get_product_price(link)
                    product_name = details[0]
                    product_price = details[1].lstrip("₹")

                    self.rowCount += 1
                    self.table.setRowCount(self.rowCount)

                    product = QTableWidgetItem(product_name)
                    product.setTextAlignment(QtCore.Qt.AlignCenter)
                    product.setFont(QtGui.QFont("family", 14))
                    self.table.setItem(self.rowCount - 1, 0, product)

                    price = QTableWidgetItem(product_price)
                    price.setTextAlignment(QtCore.Qt.AlignCenter)
                    price.setFont(QtGui.QFont("family", 13))
                    self.table.setItem(self.rowCount - 1, 1, price)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

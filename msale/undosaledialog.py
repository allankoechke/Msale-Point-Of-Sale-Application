from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.saleitemwidget import SaleWidget
from msale.icons import resources


class UndoSaleDialog(QtWidgets.QDialog):
    def __init__(self,daddy):
        QtWidgets.QDialog.__init__(self)

        self.daddy = daddy
        self.possible_list = []

        self.widget = uic.loadUi("msale/forms/undosaledialog.ui",self)
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

        self.widget.loaditemsBtn.clicked.connect(self.load_items)
        self.widget.clearBtn.clicked.connect(self.clear_all)
        self.widget.helpBtn.clicked.connect(self.help)

        self.widget.dateEdit.setDate(QtCore.QDate(QtCore.QDate.currentDate()))
        self.set_AutoComplete()
    
    def setUser(self,user):
        self.user = user

    def getUser(self):
        return self.user

    def set_AutoComplete(self):
        self.possible_list.clear() 
        self.mydb = db.Database().connect_db()
        self.cursor = self.mydb.cursor()

        sql = """SELECT item_name FROM "item" """
        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            for i in ret:
                self.possible_list.append(i[0])
            
            self.completer = QtWidgets.QCompleter(self.possible_list)
            self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            self.itemnameLE.setCompleter(self.completer)
                
        except Exception as e:
            print("Exception at Autocompletion>>",str(e))


    def load_items(self):
        self.widget.listWidget.clear()
        ind = self.widget.comboBox.currentIndex()

        if ind == 0:
            by = 'cash'
        elif ind == 1:
            by = 'mpesa'
        else:
            by = 'cashmpesa'
        
        dt = self.widget.dateEdit.date()
        dte = '{}-{}-{}'.format(dt.year(),dt.month(),dt.day())
        sql_load = """SELECT timestamp_, order_qty FROM "orders" WHERE payment_by = '{}' AND order_date = '{}' AND\
            item_name = '{}'""".format(by,dte,self.widget.itemnameLE.text())
        sql_ = """SELECT count(timestamp_) FROM "orders" WHERE payment_by = '{}' AND order_date = '{}' AND item_name =\
             '{}'""".format(by,dte,self.widget.itemnameLE.text())
        
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute(sql_)
            ret = self.cursor.fetchone()

            if ret[0] != 0:

                self.cursor.execute(sql_load)
                ret = self.cursor.fetchall()

                for row in ret:
                    tme = row[0]
                    qty = row[1]

                    if tme.hour < 10:
                        hr = '0{}'.format(tme.hour)
                    else:
                        hr = '{}'.format(tme.hour)

                    if tme.minute < 10:
                        min = '0{}'.format(tme.minute)
                    else:
                        min = '{}'.format(tme.minute)

                    time = hr+':'+min

                    # make string to display in the list widget
                    widgt = SaleWidget(self,time,qty,tme,self.widget.itemnameLE.text())

                    x = QtWidgets.QListWidgetItem() 
                    x.setSizeHint(QtCore.QSize(x.sizeHint().width(),62))
                    self.widget.listWidget.addItem(x)
                    self.widget.listWidget.setItemWidget(x,widgt)
            else:
                self.message('Empty set ... ',"No item found that satisfies the given parameters")

        except Exception as a:
            print('Error Adding to list',a)

    def message(self,n,m):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))
        msg.setWindowTitle(n)
        msg.setStyleSheet("*{background-color:rgb(54,54,54);color:white;font: 12pt \"MS Shell Dlg 2\";}\
            QPushButton{border-radius:1px;border:1px solid grey;min-height:34px;\
                min-width:50px;}\
                QPushButton:hover{border:2px solid white;}\
                    QPushButton:pressed{border:3px solid orange;}")
        msg.setText(m)
        msg.exec_()

    def clear_all(self):
        self.widget.itemnameLE.setText("")
        self.widget.comboBox.setCurrentIndex(0)
        self.widget.listWidget.clear()
        self.widget.dateEdit.setDate(QtCore.QDate(QtCore.QDate.currentDate()))

    def help(self):
        txt = "Select the item sell date, payment mode and item name \nthen click on load items. Find the \ncorrect item by quantity and time and click on undo sale."
        self.message("Help ...",txt)

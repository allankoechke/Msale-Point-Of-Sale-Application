from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources


class SaleWidget(QtWidgets.QWidget):
    def __init__(self,daddy,x,y,stp,nme):
        QtWidgets.QWidget.__init__(self)

        self.daddy = daddy
        self.timestamp = stp
        self.name = nme

        self.widget = uic.loadUi("msale/forms/saleitemwidget.ui",self)
        self.widget.undosaleBtn.clicked.connect(self.undo_sale_item)

        self.widget.timeLbl.setText(x)
        self.widget.qtyLbl.setText(str(y))

    def undo_sale_item(self):

        user = self.daddy.getUser()
        if user[2] == 3:
            self.mydb = db.Database().connect_db()
            self.cursor = self.mydb.cursor()


            old_qty = int(self.widget.qtyLbl.text())
            getqty = """SELECT stock_qty FROM "stock" WHERE item_name = \
                '{}'""".format(self.name)

            try:
                self.cursor.execute(getqty)
                ret = self.cursor.fetchone()
                new_qty = old_qty + ret[0]

                sql = """DELETE FROM "orders" WHERE item_name = '{}' AND timestamp_ = '{}'\
                    """.format(self.name,self.timestamp)
                sql_upd = """UPDATE "stock" SET stock_qty = '{}' WHERE item_name = '{}'\
                    """.format(new_qty,self.name)

                self.cursor.execute(sql)
                self.cursor.execute(sql_upd)
                
                self.mydb.commit()
                txt = "{} items of {} successfully returned to Stock from Sales".format(old_qty,self.name)
                self.message(txt,"Success ...")
                self.daddy.load_items()

            except Exception as e:
                print(e)
                self.mydb.rollback()

        else:
            txt = "This action is done by Database Administrators Only, Switch to such an account to complete action!"
            self.message(txt,"Error Processing Request")
            self.daddy.clear_all()
            self.daddy.close()

    def message(self,m,n):
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


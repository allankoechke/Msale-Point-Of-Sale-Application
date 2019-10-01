from PyQt5 import QtWidgets,QtCore,QtGui, QtPrintSupport
from msale.database import db
import pendulum, os, datetime, subprocess

from msale.icons import resources

class XP(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.cursor = db.Database().connect_db().cursor()

    def generate_price_list(self):
        tableWidget_pl = QtWidgets.QTableWidget(self)
        tableWidget_pl.setColumnCount(3)
        tableWidget_pl.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        tableWidget_pl.setHorizontalHeaderItem(0, item)
        tableWidget_pl.horizontalHeaderItem(0).setText("Item Name")

        item = QtWidgets.QTableWidgetItem()
        tableWidget_pl.setHorizontalHeaderItem(1, item)
        tableWidget_pl.horizontalHeaderItem(0).setText("Buying Price")

        item = QtWidgets.QTableWidgetItem()
        tableWidget_pl.setHorizontalHeaderItem(2, item)
        tableWidget_pl.horizontalHeaderItem(2).setText("Selling Price")

        sql = """SELECT item_name, item_bp, item_sp FROM "item" ORDER BY item_name ASC """
        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()

            for row in ret:
                i = tableWidget_pl.rowCount()
                tableWidget_pl.insertRow(i)
                tableWidget_pl.setItem(i,0,QtWidgets.QTableWidgetItem(str(row[0])))
                tableWidget_pl.setItem(i,1,QtWidgets.QTableWidgetItem(str(row[1])))
                tableWidget_pl.setItem(i,2,QtWidgets.QTableWidgetItem(str(row[2])))

            self.out_toPdf(tableWidget_pl)
        except Exception as e1:
            print("Failed to generate price list :: "+str(e1))

    def out_toPdf(self,table):
        # prints the customer receipts to a pdf 
        # file or to an external printer

        date = self.get_date()
        html = u""
        html += """
                <!DOCTYPE html>
                <html>
                    <h1 style="text-align:center">Chebui Agrovet</h1>
                    <h2 style="text-align:center">For Better Animal Health And Productivity</h2>
                    <h3 style="text-align:center">P.O. BOX 32,Kabiyet</h3>
                    <h4 style="text-align:center">{}</h4>
                    <body>
                        <div>
                            <table border= '1' width="100%" cellpadding="0" cellspacing="0">
                                <caption>{}</caption>
                                <tr>
                                    <th style="padding: 6px;">No.</th>
                                    <th style="padding: 6px;">Product Name</th>
                                    <th style="padding: 6px;">Buying Price</th>
                                    <th style="padding: 6px;">Selling Price</th>
                                </tr>""".format(date,"Price List 2019")

        row = table.rowCount()
        for i in range(row):
            n = table.item(i,0).text()
            p = table.item(i,1).text()
            q = table.item(i,2).text()
            txt = "{}.".format(i+1)

            html += """
                <tr>
                    <td style="border:1px solid black;padding: 6px;">{}</td>
                    <td style="border:1px solid black;padding: 6px;">{}</td>
                    <td style="border:1px solid black;padding: 6px;">{}</td>
                    <td style="border:1px solid black;padding: 6px;">{}</td>
                </tr>
                """.format(txt,n,p,q)
        html += """
                        </table>
                    </div>
                    <br>
                </body>
            </html>"""
            
        _a = pendulum.now()
        name_ = "pricelist_{}-{}-{}".format(_a.year,_a.month,_a.day)

        Print(html,name_)

    def get_date(self):
        date = pendulum.now()
        ls1 = [1,21,31]
        ls2 = [2,22]
        ls3 = [3,23]
        day_ = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        if date.day in ls1:
            s = 'st'
        elif date.day in ls2:
            s = 'nd'
        elif date.day in ls3:
            s = 'rd'
        else:
            s = 'th'
        for x in range(len(day_)):
            if date.day_of_week == x:
                day__ = day_[x]
        m = datetime.datetime.now()
        mnth = m.strftime("%B")
        dte = "{}<sup>{}</sup> {} {}, {}".format(date.day,s,day__,mnth,date.year)
            
        return dte

class Print:
    # Class to handle printing of receipts and other stuff

    def __init__(self,html,name):
        self.html = html
        self.name = name
        self.setup_printer()   

    def setup_printer(self):
        # check output path location

        pthx = "{}\\My Documents\\.MySale-Output-Files".format(os.path.expanduser("~"))

        if os.path.isdir(pthx) == False:
            os.makedirs(pthx)

        self.printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        self.printer.setPageSize(QtPrintSupport.QPrinter.Letter)
        self.printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        pth = "{}\\{}.pdf".format(pthx,self.name)
        self.printer.setOutputFileName(pth)
        try:
            doc = QtGui.QTextDocument()
            doc.setHtml(self.html)
            doc.print_(self.printer)
            
            m = 'explorer "{}"'.format(pthx)
            subprocess.Popen(m)

        except Exception as a:
            msg = "Error printing to pdf, "+str(a)
            t = "Error..."
            ico = QtWidgets.QMessageBox.Warning
            self.show_message(msg,ico,t)

    def show_message(self,msg,ico,t):
        # display error messages 
        a = QtWidgets.QMessageBox()
        a.setStyleSheet("font: 12;")
        a.setText(msg)
        a.setWindowTitle(t)
        a.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))
        a.setStandardButtons(QtWidgets.QMessageBox.Ok)
        a.exec_()
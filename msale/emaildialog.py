from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources
import os, ssl, smtplib


class EmailDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.widget = uic.loadUi("msale/forms/emaildialog.ui",self)
        self.widget.sendBtn.clicked.connect(self.email_sent)

        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

    def email_sent(self):
        if len(self.widget.emailLE.text()) == 0:
            msg = "Your Email Field Is Empty"
            self.show_message(msg,1)

        elif len(self.widget.subjectLE.text()) == 0:
            msg = "Subject Field Is Empty"
            self.show_message(msg,1)

        elif len(self.widget.textEdit.toPlainText()) == 0:
            msg = "Body Field Is Empty"
            self.show_message(msg,1)

        else:
            self.sent = False

            port = 465
            smtp_server = "smtp.gmail.com"
            sender_email = "myappslalan@gmail.com"
            receiver_email = "lalan2205@gmail.com"
            password = "myappslalan2019"
            message = """
            Subject: {}


            {}
            Sent From : {} of MySale App
            """ .format(self.subjectLE.text(),self.widget.textEdit.toPlainText(),self.widget.emailLE.text())
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL(smtp_server,port,context = context) as server:
                    server.login(sender_email,password)
                    server.sendmail(sender_email,receiver_email,message)
                    self.show_message("Email Sent Successfully!",0)
                    self.widget.subjectLE.setText("")
                    self.widget.emailLE.setText("")
                    self.widget.textEdit.setText("")

            except :
                self.show_message("Couldn't send Email,Check Your Internet Connection",2)

    def show_message(self,x,y):
        msg = QtWidgets.QMessageBox()
        msg.setText(x)
        msg.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))
        if y != 0:
            msg.setWindowTitle("Error Sending Mail")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
        else:
            msg.setWindowTitle("Success Sending Mail")
            msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()


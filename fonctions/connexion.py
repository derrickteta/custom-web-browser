from PyQt5.QtWidgets import (QLineEdit, QApplication, QWidget, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QMessageBox)
 
class Ui_RegisterForm(QWidget):
    def __init__(self):
        super(Ui_RegisterForm, self).__init__()
        self.setupUi()
     
    def setupUi(self):
        self.setFixedSize(300, 200)
        self.setWindowTitle("Make a new account")
         
        self.Usernameedit = QLineEdit()
        self.Passwordedit = QLineEdit()
        self.confirmPasswordedit = QLineEdit()
        self.Passwordedit.setEchoMode(QLineEdit.Password)
        self.confirmPasswordedit.setEchoMode(QLineEdit.Password)
         
        self.confirmButton = QPushButton()
        self.cancelButton = QPushButton()
        self.confirmButton.clicked.connect(self.getValues)
        self.cancelButton.clicked.connect(lambda: self.close())
 
        self.confirmButton.setText("Confirm")
        self.cancelButton.setText("Cancel")
        self.Usernameedit.setPlaceholderText("Username")
        self.Passwordedit.setPlaceholderText("Password")
        self.confirmPasswordedit.setPlaceholderText("Confirm Password")
        self.confirmPasswordedit.returnPressed.connect(self.getValues)
         
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.Usernameedit)
        vbox.addWidget(self.Passwordedit)
        vbox.addWidget(self.confirmPasswordedit)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.confirmButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
         
    def getValues(self):
        if self.Passwordedit.text() == self.confirmPasswordedit.text():
            values = [self.Usernameedit.text(), self.Passwordedit.text(), self.confirmPasswordedit.text()]
            # use the values for the next step
            print(values) # for testing only
            self.close()
        else:
            msg = QMessageBox.warning(None, "Error", "passwords not matching" )
            return
             
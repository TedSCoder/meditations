from PyQt5.QtWidgets import QMessageBox, QPushButton

# makes error dialog, returns the object
def file_error_msg():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText("Error Opening File")
    msg.setInformativeText("Please close all open instances of journal files before starting this program")

    return msg

# makes no journal warning dialog, returns the object
def no_journal_msg():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning")
    msg.setText("There is no journal entry here")

    return msg

# asks if user really want to delete the journal entry
def del_journal_msg():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning")
    msg.setText("Do you want to delete journal entry?")
    msg.addButton(QPushButton('Accept'), QMessageBox.YesRole)
    msg.addButton(QPushButton('Reject'), QMessageBox.NoRole)

    return msg
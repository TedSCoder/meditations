#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Stoic Journaling Software, Meditations Alpha Version
   Author: Ted Shin
   Date: Dec 28, 2019
   Comments: This is something I wrote to help me journal and become a better daily
            stoic. The journaling format is roughly what Marcus Aurelius followed
            in his journal Meditations. I tried writing journals via pen and paper,
            but I really prefer typing it out and also I want to make my own program
            to help me out.
"""


# sys and os
import sys
import os.path
from os import path

# PyQt5 dependencies
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QDialogButtonBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

# custom widget, not used here but Pyinstaller doesnt understand ui file needs this,
# so putting it here to make it fetch the right dependencies
from customcalendar import CustomCalendar

# Beautiful Soup
from bs4 import BeautifulSoup

# Error funcs
from errors_warnings import *


# Translate asset paths to useable format for PyInstaller
def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)


# This is the main window for the application
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def initUI(self):
        # set up directory, check for file integrity
        self.file_exists = set()
        self.set_config()
        # load ui
        uic.loadUi(resource_path("qt_ui/meditations.ui"),self)

        # set icons for push buttons
        self.edit.setIcon(QIcon(QPixmap(resource_path('images/pen_icon.png'))))
        self.edit.setIconSize(QSize(120, 120))

        self.read.setIcon(QIcon(QPixmap(resource_path('images/read_icon.png'))))
        self.read.setIconSize(QSize(120, 120))

        # update current date
        self.curr_qdate = self.calendar.selectedDate()

        #button clicks
        self.calendar.clicked.connect(self.clicked_date)
        self.edit.clicked.connect(self.edit_journal)
        self.read.clicked.connect(self.read_journal)

    # updates clicked date on the calendar
    def clicked_date(self,date):
        self.curr_qdate = date

    # edit journal signal, invokes edit journal dialog
    def edit_journal(self):
        entry = JournalDialog(self.curr_qdate, self.curr_qdate.toString("yyyy-MM-dd") in self.file_exists)
        entry.exec_()

        # update the calender dot marker
        if entry.new:
            self.calendar.journals.add(self.curr_qdate)
            self.file_exists.add(self.curr_qdate.toString("yyyy-MM-dd"))

        if entry.deleted:
            self.calendar.journals.remove(self.curr_qdate)
            self.file_exists.remove(self.curr_qdate.toString("yyyy-MM-dd"))



    # open up journal reader
    def read_journal(self):
        if self.curr_qdate.toString("yyyy-MM-dd") in self.file_exists:
            self.reader = JournalReader(self.curr_qdate)
            self.reader.show()
        else:
            no_journal_msg().exec_()

    # This sets up config file and journal repository if one does not exist
    # also checks for file integrity based on what config says and what dir are available
    # Lastly, this sets up hashmap for existence of files, removes duplicate entries with same date name in config
    def set_config(self):
        # check if journal path directories exist, if not make them
        if not path.exists("journal_repository"):
            os.mkdir("journal_repository")

        # load journal entries from config file
        try:
            if path.exists("config.txt"):
                config = open("config.txt","r")
                temp = open("tmp.txt","w+")
                # read config file
                lines = config.readlines()

                # check consistency of files, whether files missing or not versus what config file says
                for line in lines:
                    info = line.split('\t')
                    if bool(info[1]) == True and path.exists("journal_repository/"+info[0] + ".txt") and info[0] not in self.file_exists:
                        self.file_exists.add(info[0]) #add to hashset
                        temp.write(info[0]+"\tTrue\n")

                #close file
                temp.close()
                config.close()
                #remove the original config file and replace with temp
                os.remove("config.txt")
                os.rename("tmp.txt","config.txt")
            #if config file doesnt exist make one
            else:
                config = open("config.txt","w+")
                config.close()

        except Exception:
            file_error_msg().exec_()


# This reads the journal, since I am using QLabel to display text, this has limitations on how many characters
# I can display on this window.
class JournalReader(QMainWindow):
    def __init__(self, date=None):
        super(JournalReader,self).__init__()
        self.date = date
        self.initUI()

    def initUI(self):
        uic.loadUi(resource_path("qt_ui/journal_reader.ui"),self)
        # set journal title
        self.title.setText("Journal Formatted Entry: " + self.date.toString())
        self.title.adjustSize()

        try:
            # read the contents of the journal
            f = open("journal_repository/" + self.date.toString("yyyy-MM-dd") + ".txt", "r")
            content = f.read()
            f.close()

            # use beautiful soup to decode text blocks/chunks
            interpretted = ""
            formatted = False
            soup = BeautifulSoup(content, "html.parser")
            for s, i in zip(soup.findAll(), range(1, 7)):
                s = BeautifulSoup.get_text(s)  # if I use soup.strings, it omits empty string within tags, so doing it this way
                if s == "": continue  # skip empty texts
                if i == 1:
                    interpretted = interpretted + " Main Entry:\n\n"

                if not formatted and i is not 1:
                    interpretted = interpretted + " Meditative Steps:\n\n"
                    formatted = True
                interpretted = interpretted + "\t" +s + "\n\n"

            self.content.setText(interpretted)
            self.content.adjustSize()

        except Exception:
            file_error_msg().exec_()


# This is the journal edit dialog class
class JournalDialog(QDialog):
    def __init__(self, date, exist=False):
        super(JournalDialog,self).__init__()
        self.date = date
        self.exist = exist
        self.new = False
        self.deleted = False
        self.initUI()

    def initUI(self):
        uic.loadUi(resource_path("qt_ui/journal_entry.ui"),self)
        # set journal title
        self.title.setText("Journal Formatted Entry: "+ self.date.toString())
        self.title.adjustSize()

        # load journal content if exists
        if self.exist:
            try:
                # read the contents of the journal
                f = open("journal_repository/"+self.date.toString("yyyy-MM-dd")+".txt","r")
                content = f.read()
                f.close()

                # use beautiful soup to decode text blocks/chunks
                soup = BeautifulSoup(content, "html.parser")
                for s, i in zip(soup.findAll(), range(1,7)):
                    s = BeautifulSoup.get_text(s) #if I use soup.strings, it omits empty string within tags, so doing it this way
                    if s == "": continue # skip empty texts
                    varname = eval("self.text"+str(i))
                    varname.setText(s)

            except Exception:
                file_error_msg().exec_()

        self.accepted.connect(self.write_to_file)
        self.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.delete_file)


    def delete_file(self):
        if self.exist:
            result = del_journal_msg().exec_()
            if result is 0:
                self.deleted = True
                os.remove("journal_repository/"+self.date.toString("yyyy-MM-dd")+".txt")
                self.close() # close the journal edit gui

        else:
            no_journal_msg().exec_()


    def write_to_file(self):
        #save journal as plain text
        try:
            f = open("journal_repository/"+self.date.toString("yyyy-MM-dd")+".txt","w+")
            for i in range(1,7):
                varname = eval("self.text"+str(i))
                f.write("<block>"+varname.toPlainText()+"</block>")
            f.close()
        except Exception:
            file_error_msg().exec_()

        # write to config file, if it didnt exist already
        if not self.exist:
            try:
                f = open("config.txt","a")
                f.write(self.date.toString("yyyy-MM-dd")+"\tTrue\n")
                f.close()
                self.new = True
            except Exception:
                file_error_msg().exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('images/icon.png')))
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
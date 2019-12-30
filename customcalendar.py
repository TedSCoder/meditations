from PyQt5.Qt import QPainter, QDate, QRect
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5 import QtGui


# had to modify qcalendarwidget to modify custom paintcell
class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super(CustomCalendar,self).__init__()
        self.load_journals()

    
    # custom paint cell, to mark down which dates have journal entry
    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        if date in self.journals:
            painter.setBrush(Qt.green)
            painter.drawEllipse(rect.topLeft() + QPoint(12, 12), 7, 7)


    # assumes config file exists, and in correct format
    def load_journals(self):
        # load journal entries from config file
        config = open("config.txt", "r")
        self.journals = set()
        # read config file
        lines = config.readlines()

        # dump into journals list
        for line in lines:
            date_info = line.split('\t')[0].split('-')
            self.journals.add(QDate(int(date_info[0]),int(date_info[1]),int(date_info[2])))

        config.close()

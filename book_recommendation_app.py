import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./book_recommendation.ui')[0]
genre = ['추리/미스터리', '공포/스릴러', '판타지', '무협', 'SF', '역사', '로맨스']

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        categories = ['장르소설', '테마소설', '한국소설']

        self.cmb_category.addItems(categories)

        self.cmb_category.activated[str].connect(lambda: self.choose_sub(self.cmb_category))

    def choose_sub(self, item):
        if item.currentText() == '장르소설':
            self.cmb_sub.clear()
            self.cmb_sub.addItems(genre)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
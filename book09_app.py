import sys
import bookImgSave
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
import random
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel
import requests

form_window = uic.loadUiType('./qt_findyourbook.ui')[0]
categories = ['장르소설', '테마소설', '고전소설', '한국소설']

df = pd.read_csv('./book_data/genre_novel.csv')
df_theme = pd.read_csv('./book_data/theme_novel.csv')
df_korean = pd.read_csv('./book_data/korean_novel.csv')
Tfidf_matrix = mmread('./models/Tfidf_book_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)
embedding_model = Word2Vec.load('./models/word2vec_genre_novel_review.models')


####################################
# df_genre = pd.read_csv('./genre_novel.csv')
# genre_sub = df['sub_category'].unique()
# mystery = df[df['sub_category'] == '추리/미스터리']
# horror = df[df['sub_category'] == '공포/스릴러']
# fantasy = df[df['sub_category'] == '판타지']
# martial_arts = df[df['sub_category'] == '무협']
# sf = df[df['sub_category'] == 'SF']
# history = df[df['sub_category'] == '역사']
# romance = df[df['sub_category'] == '로맨스']

# theme_sub_categories = ['성장소설/가족소설', '연애/사랑소설', '웹소설', '보이러브', '어른을 위한 동화/우라이트 노벨', '영화와 드라마 원작']
# classic_sub_categories = ['한국 고전문학', '동양 고전문학', '서양 고전문학', '신화와 설화']
# korea_sub_categories = ['한국 단편소설', '한국 장편소설']
# df_image = df.loc['title', 'image_path']

# image = requests.get('https://image.yes24.com/goods/3337930/XL')
# print(image.content)
# with open('./img/photo.jpg', 'wb') as f:
#     f.write(image.content)

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cmb_category.addItems(categories)
        self.cmb_category.activated[str].connect(lambda: self.choose_category(self.cmb_category))
        self.btn_result.clicked.connect(lambda: self.show_result(self.le_keyword))
        self.checkBox.stateChanged.connect(self.keyword_activate)

        model = QStringListModel()
        model.setStringList(embedding_model.wv.index_to_key)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)

    def keyword_activate(self):
        if self.checkBox.checkState():
            self.cmb_sub.setEnabled(False)
            self.cmb_sub.clear()
            self.le_keyword.setEnabled(True)
        else:
            self.le_keyword.clear()
            self.cmb_sub.setEnabled(True)
            self.le_keyword.setEnabled(False)

    def show_result(self, keyword):
        if not keyword.text():
            if self.cmb_sub.currentText():
                sub_category = df[df['sub_category'] == self.cmb_sub.currentText()]
                bookImgSave.img_save(sub_category)
                self.lbl_result1.setPixmap(QPixmap('./img/result1.jpg'))
                self.lbl_result2.setPixmap(QPixmap('./img/result2.jpg'))
        else:
            try:
                recommendation = self.recommendation_by_keyword(keyword.text())
                recommendation = recommendation.iloc[random.sample(range(20), 2)]
                title1 = recommendation.iloc[0]
                title2 = recommendation.iloc[1]
                image1 = df[df['title'] == title1].iloc[0].image_path
                image2 = df[df['title'] == title2].iloc[0].image_path
                result1 = requests.get(image1)
                result2 = requests.get(image2)
                with open('./img/result1.jpg', 'wb') as f:
                    f.write(result1.content)
                with open('./img/result2.jpg', 'wb') as f:
                    f.write(result2.content)
                self.lbl_result1.setPixmap(QPixmap('./img/result1.jpg'))
                self.lbl_result2.setPixmap(QPixmap('./img/result2.jpg'))
            except:
                self.lbl_result1.setText('제가 모르는 단어입니다.')
                self.lbl_result2.setText('제가 모르는 단어입니다.')

    def recommendation_by_keyword(self, key_word):
        try:
            sim_word = embedding_model.wv.most_similar(key_word, topn=20)
        except:
            self.lbl_result1.setText('제가 모르는 단어입니다.')
            self.lbl_result2.setText('제가 모르는 단어입니다.')
            return
        words = [key_word]
        for word, _ in sim_word:
            words.append(word)
        sentence = []
        count = 10
        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        sentence_vec = Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
        recommendation = self.get_recommendation(cosine_sim)
        # recommendation = '\n'.join(list(recommendation))

        return recommendation

    def get_recommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:20]
        movieIdx = [i[0] for i in simScore]
        recbookList = df.iloc[movieIdx, 0]
        return recbookList[:20]

    def choose_category(self, text):
        if text.currentText() == '장르소설':
            self.cmb_sub.clear()
            self.cmb_sub.addItems(df.sub_category.unique())
        elif text.currentText() == '테마소설':
            self.cmb_sub.clear()
            self.cmb_sub.addItems(df_theme.sub_category.unique())
        elif text.currentText() == '고전소설':
            self.cmb_sub.clear()
        elif text.currentText() == '한국소설':
            self.cmb_sub.clear()
            self.cmb_sub.addItems(df_korean.sub_category.unique())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())

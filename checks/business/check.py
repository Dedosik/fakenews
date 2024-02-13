# -*- coding: utf-8 -*-
import numpy as np
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound

#  --- ОБУЧЕНИЕ ---
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'FakeNewsNet.csv')
data = pd.read_csv(file_path)
# data["fake"] = data["label"].apply(lambda x: 0 if x == "REAL" else 1)
# data = data.drop("label", axis=1)


X, y = data["title"], data["real"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

clf = LinearSVC()
clf.fit(X_train_vectorized, y_train)

accuracy = clf.score(X_test_vectorized, y_test)


def is_fake(news_title):
    #  --- ПЕРЕВОД НОВОСТИ НА АНГЛИЙСКИЙ ---
    text = ""
    while not text:
        try:
            text += GoogleTranslator(source="ru", target="en").translate(news_title)
        except TranslationNotFound:
            pass

    #  --- ПРЕДСКАЗАНИЕ ---
    vectorized_text = vectorizer.transform([text])
    predict = clf.predict(vectorized_text)[0]

    return 0 if predict else 1




"""Genererate tags for recipes

This code is based on Jeremy Howards' Strong linear baseline available here:
https://www.kaggle.com/jhoward/nb-svm-strong-linear-baseline
"""

import re
import string
import numpy as np
import pandas as pd

from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

# For test
FILE_LOC: str = '/home/krispin/data/improved-happiness/'
# For dev
#FILE_LOC: str = '/home/krispin/data/improved-happiness/proto/'
LABEL_COLS = ['Peanut Free',
 'Soy Free',
 'Bon Appétit',
 'Tree Nut Free',
 'Vegetarian',
 'Kosher',
 'Pescatarian',
 'Gourmet',
 'Quick & Easy',
 'Wheat/Gluten-Free']
PREP = 'preparation_steps'
re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')


def tokenize(s):
    return re_tok.sub(r' \1 ', s).split()


def pr(x, y_i, y):
    p = x[y == y_i].sum(0)
    return (p+1) / ((y == y_i).sum()+1)


def get_model(x, y):
    y = y.values
    r = np.log(pr(x, 1, y) / pr(x, 0, y))
    m = LogisticRegression(C=4, dual=True, solver='liblinear')
    x_nb = x.multiply(r)
    return m.fit(x_nb, y), r


def main():
    filename = FILE_LOC + 'recipe_tags.csv'
    df = pd.read_csv(filename)
    X_train, X_test, y_train, y_test = train_test_split(
        df[PREP], df[LABEL_COLS], test_size=0.33, random_state=42)

    assert not X_train.isnull().any()

    vec = TfidfVectorizer(ngram_range=(1, 2), tokenizer=tokenize,
                          min_df=3, max_df=0.9, strip_accents='unicode', use_idf=1,
                          smooth_idf=1, sublinear_tf=1)
    trn_term_doc = vec.fit_transform(X_train)
    test_term_doc = vec.transform(X_test)

    preds = np.zeros((len(X_test), len(LABEL_COLS)))
    for i, j in enumerate(LABEL_COLS):
        m, r = get_model(trn_term_doc, y_train[j])
        preds[:, i] = m.predict_proba(test_term_doc.multiply(r))[:, 1]
        print('fitted', j)
    #Calculate ROC
    score = roc_auc_score(y_test, preds)
    print(f'ROC-AUC score for tag gen is {score:.3f}')
    

if __name__ == '__main__':
    main()

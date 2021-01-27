import numpy as np
import pandas as pd

train_file = open("train.csv")

train_df = pd.read_csv(train_file)

target = train_df['category']

X = train_df.values.tolist()
Y = []

for val in target:
    if val == 'close':
        Y.append(0)
    else:
        Y.append(1)

for array in X:
    try:
        array.remove('close')
    except ValueError:
        try: 
            array.remove('far')
        except ValueError:
            pass

X = np.array(X)
Y = np.array(Y)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X,Y, train_size=0.625)

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

clf = RandomForestClassifier(n_estimators=50)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
print(accuracy_score(y_test, y_pred))
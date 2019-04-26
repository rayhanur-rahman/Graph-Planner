import numpy as np, random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
import timeit, math, os
from sklearn.ensemble import RandomForestClassifier

def learn(trainFile, testFile, training_size, depth, leaf, split):
    start = timeit.default_timer()
    trainData = pd.read_csv(trainFile,sep= ',', header=None)
    testData = pd.read_csv(testFile,sep= ',', header=None)

    size = trainData.shape[0]
    predictor_train = trainData.values[0:math.ceil((training_size*size)/100), 1:]
    response_train = trainData.values[0:math.ceil((training_size*size)/100):,0]

    predictor_test = testData.values[:, 1:]
    response_test = testData.values[:, 0]


    clf_entropy = DecisionTreeClassifier(criterion = "entropy",
                                     random_state = 100,
                                     max_depth=depth,
                                     min_samples_leaf=leaf,
                                     min_samples_split=split)


    clf_entropy.fit(predictor_train, response_train)
    end = timeit.default_timer()
    y_pred_en = clf_entropy.predict(predictor_test)

    ifa = 0
    tpFound = False
    for x in range(0, len(y_pred_en)):
        if y_pred_en[x] == 1.0 and response_test[x] == 0.0 and tpFound == False: ifa += 1
        if y_pred_en[x] == 1.0 and response_test[x] == 1.0: tpFound = True

    print(f'accuracy: {accuracy_score(response_test, y_pred_en)}')
    cf = confusion_matrix(response_test, y_pred_en)
    print(cf)
    print(classification_report(response_test, y_pred_en))

    accuracy = (cf[1][1]+cf[0][0])/(cf[0][0]+cf[1][1]+cf[0][1]+cf[1][0])
    precision = cf[1][1]/(cf[1][1]+cf[0][1]+.001)
    recall = cf[1][1]/(cf[1][1]+cf[1][0])
    falseAlarm = cf[0][1]/(cf[0][1]+cf[0][0])
    d2h = math.sqrt((1-recall)*(1-recall) + falseAlarm*falseAlarm)
    f1score = (2*precision*recall)/(precision+recall+.001)

    return [accuracy, precision, recall, f1score]


x = learn('s.csv', 'st.csv', 100, 22, 1, 2)
print(x)
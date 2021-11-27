# Preprocessing data and traing KNN ML model using train data and predicting output for test data

# Importing required modules
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

class ModelDT:
    # Function   :- initializing KNN model object and two variables minS and maxS 
    def __init__(self):
        self.__knn = DecisionTreeClassifier()
        self.__minS = 0
        self.__maxS = 0
    
    # Function   :- preprocesses data and give it to ML model
    #
    # Parameters :- X - DataFrame containing all the features
    #               isTrain - True if it is train data
    #                         False if it is test data
    #
    # Returns    :- DataFrame of processed data
    def __preprocess(self, X: pd.DataFrame, isTrain=False):
        X = self.__scale(X, fit=isTrain)
        return X

    # Function   :- scales data
    #
    # Parameters :- X - DataFrame containing all the features
    #               fit - True if it is train data
    #                     False if it is test data
    #
    # Returns    :- DataFrame of scalled data
    def __scale(self, X, fit=False):
        if fit:
            self.__minS = np.min(X)
            self.__maxS = np.max(X)
        X = (X - self.__minS)/(self.__maxS-self.__minS)
        return X

    # Function   :- trains KNN model
    #
    # Parameters :- X - DataFrame containing all the features
    #               y - Series containing target
    def train(self, X: pd.DataFrame, y:pd.Series):
        # TODO preprocessing
        X = self.__preprocess(X, isTrain=True)
        # TODO train model
        self.__knn = self.__knn.fit(X, y)

        y_pred = self.__knn.predict(X)

        # Printing confusion matrix and accuracy of model
        print("Confusion matrix :-- \n", confusion_matrix(y, y_pred))
        print("Score :-- ", self.__knn.score(X, y))

    # Function   :- predicts output for test data using trained KNN model
    # Parameters :- X - DataFrame containing all the features
    # Returns    :- numpy array containing predicted output by model
    def pred(self, X:pd.DataFrame):
        # TODO preprocessing
        X = self.__preprocess(X, isTrain=False)

        # TODO return predictions using model
        return self.__knn.predict(X)
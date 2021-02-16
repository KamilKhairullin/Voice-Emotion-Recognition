import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from NeuralNetworks.MLPC import MLPC
from DataLoading.DataLoader import DataLoader
from NeuralNetworks.CNN import CNN
import numpy as np

def runCNNExample(pathToData):
    cnn = CNN(2)
    dataLoader = DataLoader(pathToData, 0.25)
    x_train,x_test,y_train,y_test = dataLoader.loadData()
    x_train,x_test,y_train,y_test = cnn.prepareData(x_train,x_test,y_train,y_test)
    cnn.fit(x_train, y_train, 15)
    y_pred = cnn.predict(x_test)
    cnn.printStats(y_test, y_pred)

def runMLPCExample(pathToData):
    mlpc = MLPC()
    dataLoader = DataLoader(pathToData, 0.25)
    x_train,x_test,y_train,y_test = dataLoader.loadData()
    mlpc.fit(x_train, y_train)
    y_pred = mlpc.predict(x_test)
    mlpc.printStats(y_test, y_pred)

pathToData = 'data'
runMLPCExample(pathToData)
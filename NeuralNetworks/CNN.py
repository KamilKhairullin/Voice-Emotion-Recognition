import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.layers import Input, Flatten, Dropout, Activation, BatchNormalization, Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import to_categorical
from tensorflow.keras.optimizers import RMSprop
from sklearn.preprocessing import LabelEncoder
from keras.regularizers import l2

class CNN:

    def __init__(self, classes, inputShape = (180, 1)):
        self.model = self.__makeModel(inputShape, classes, 'sigmoid')
        self.__compile()

    def __makeModel(self, inputShape, classes, activationFunction='sigmoid'):
        model = Sequential()
        model.add(Conv1D(256, kernel_size=(10), activation='relu', input_shape=inputShape))
        model.add(Conv1D(256, kernel_size=(10),activation='relu',kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
        model.add(MaxPooling1D(pool_size=(8)))
        model.add(Dropout(0.3))
        model.add(Conv1D(128, kernel_size=(10),activation='relu'))
        model.add(MaxPooling1D(pool_size=(8)))
        model.add(Dropout(0.3))
        model.add(Flatten())
        model.add(Dense(356, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(classes, activation='sigmoid'))
        return model

    def __compile(self):
        optimizer = RMSprop(lr=1e-5, decay=1e-7)
        self.model.compile(loss='categorical_crossentropy',
                                optimizer=optimizer,
                                metrics=['accuracy'])

    def fit(self, x_train, y_train, epochs):
        self.model.fit(x_train,y_train, epochs=epochs)
        print('Data fitted.')

    def predict(self, x_test):
        return self.model.predict(x_test)

    def prepareData(self, x_train, x_test, y_train, y_test):
        x_train = x_train.reshape(np.shape(x_train)[0], 180, 1)
        x_test = x_test.reshape(np.shape(x_test)[0], 180, 1)

        lb = LabelEncoder()
        y_train = to_categorical(lb.fit_transform(y_train))
        y_test = to_categorical(lb.fit_transform(y_test))
        return x_train, x_test, y_train, y_test

    def printStats(self, y_test, y_pred):
        cnt = 0
        for i in range(len(y_pred)):    
          result = np.squeeze(y_pred[i])
          resultIndex = np.argmax(y_pred[i])
          if np.argmax(y_pred[i]) == np.argmax(y_test[i]):
            cnt = cnt + 1
        result = cnt / len(y_pred)
        print("Accuracy: {:.2f}%".format(result*100))
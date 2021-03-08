from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle


class MLPC:

    def __init__(self, alpha=0.01, batch_size=256, epsilon=1e-08,
                 hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500):
        self.model = MLPClassifier(alpha=alpha, batch_size=batch_size, epsilon=epsilon,
                                   hidden_layer_sizes=hidden_layer_sizes, learning_rate=learning_rate,
                                   max_iter=max_iter)

    def fit(self, x_train, y_train):
        self.model.fit(x_train, y_train)
        print('Data fitted.')

    def predict(self, x_test):
        return self.model.predict_proba(x_test)

    def printStats(self, y_test, y_pred):
        result = accuracy_score(y_true=y_test, y_pred=y_pred)
        print("Accuracy: {:.2f}%".format(result * 100))
        return result

    def saveModel(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self.model, f)

    def loadModel(self, path):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)

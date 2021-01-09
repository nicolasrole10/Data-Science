from sklearn.datasets import make_regression
import numpy as np
from functools import reduce

def add_intercept(x):
    return np.insert(x,0,1)

def squared(x):
    return x**2

def get_features(feature):
    return np.array([i[feature] for i in model.features])

def get_derivative(feature):
    return np.multiply(get_features(feature),model.model_error)

def get_learn(feature):
    return reduce(lambda a,b: a+b, get_derivative(feature)) / model.m

class model_():
    def __init__(self,data):
        self.features = data[0]
        self.output = data[1]
        self.m = len(data[1])
        self.test_error = 1

    def intercept(self):
        self.features = np.array(list(map(add_intercept,self.features)))

    def beta_parameters(self):
        self.beta_parameters_ = np.array(list([100.0,100.0,100.0,100.0]))

    def learning_rate(self,lr):
        self.learning_rate_ = lr

    def predict(self):
        self.predictions_ = self.features.dot(self.beta_parameters_)

    def errors(self):
        self.model_error = np.array(list(self.predictions_ - self.output))
        self.test_error = reduce(lambda a,b: a+b,self.model_error)
        self.model_squared_error = reduce(lambda a,b: a+b, np.array(list(map(squared,self.model_error))))

    def update_betas(self):
        self.beta_parameters_[0] = self.beta_parameters_[0] - (self.learning_rate_ * get_learn(0))
        self.beta_parameters_[1] = self.beta_parameters_[1] - (self.learning_rate_ * get_learn(1))
        self.beta_parameters_[2] = self.beta_parameters_[2] - (self.learning_rate_ * get_learn(2))
        self.beta_parameters_[3] = self.beta_parameters_[3] - (self.learning_rate_ * get_learn(3))

model = model_(make_regression(n_samples=100,n_features=3,n_targets=1,n_informative=3,random_state=5))
model.intercept()
model.beta_parameters()
model.learning_rate(0.5)
iterations = 0
while model.test_error > 0 and model.test_error > 0.000000001:
    model.predict()
    model.errors()
    print('Model_squared_error', model.model_squared_error)
    print('Betas_antiguos', model.beta_parameters_)
    print('Model_Error', model.test_error)
    model.update_betas()
    iterations += 1
    print('************************************************')
    print('************************************************')
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt

dataset = pd.read_csv("C:\\Users\dufresnej2\Desktop\AutoDock\ZINC\\full_database.csv")

X = dataset[['logp', 'mwt', 'tpsa', 'rotbonds']]
y = dataset['bindaff']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

mlr = LinearRegression()
mlr.fit(x_train, y_train)

# print("Intercept: ", mlr.intercept_)
# print("Coefficients:")
# print(list(zip(X, mlr.coef_)))

y_pred_mlr = mlr.predict(x_test)
print("Prediction for test set: {}".format(y_pred_mlr))

mlr_diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': y_pred_mlr})
print(mlr_diff.head())

meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
print('R squared: {:.2f}'.format(mlr.score(X, y)*100))
print('Mean Absolute Error:', meanAbErr)
print('Mean Square Error:', meanSqErr)
print('Root Mean Square Error:', rootMeanSqErr)


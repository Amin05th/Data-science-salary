import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import statsmodels.api as sm


df = pd.read_csv('eda_data.csv')

# choose relevant columns
df_model = df[['salary', 'company_size', 'company_industry', 'company_sector', 'company_revenue', 'hourly', 'monthly',
               'location', 'age', 'python_yn', 'spark', 'aws', 'excel', 'job_simp', 'seniority', 'desc_len']]
# get dummy data

df_dum = pd.get_dummies(df_model)

# train test split
X = df_dum.drop('salary', axis=1)
y = df_dum.salary.values
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.2, random_state=42)

# multiple linear regression
X_sm = X = sm.add_constant(X)
model = sm.OLS(y, X_sm)
model.fit().summary()

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train, y_train, scoring="neg_mean_absolute_error", cv=3))
# lasso regression
lm_l = Lasso(alpha=.13)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring="neg_mean_absolute_error", cv=3))
alpha = []
error = []

for i in range(1, 100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring="neg_mean_absolute_error", cv=3)))

plt.plot(alpha, error)
plt.show()
err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=["alpha", "error"])
df_err[df_err.error == max(df_err.error)]
# random forest
rf = RandomForestRegressor()
np.mean(cross_val_score(rf, X_train, y_train, scoring="neg_mean_absolute_error", cv=3))

# tune models GridsearchCV
parameters = {'n_estimators': range(10, 300, 10), 'criterion': ('absolute_error', 'friedman_mse', 'poisson', 'squared_error'), 'max_features': [.5]}
gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)

gs.best_score_
gs.best_estimator_
# test ensembles

tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, tpred_rf)
mean_absolute_error(y_test, (tpred_lm+tpred_rf/2))

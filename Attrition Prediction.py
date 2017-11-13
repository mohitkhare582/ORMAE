import pandas as pd
import numpy as np
from  keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Dropout
import math
from sklearn import preprocessing

df = pd.read_csv("HR_Employee_Attrition_Data.csv")
Rtrain = pd.DataFrame(df['Attrition'])
for y in range(len(Rtrain['Attrition'])):
    if Rtrain["Attrition"][y] == 'Yes':
        Rtrain["Attrition"][y] = 1
    else:
        Rtrain["Attrition"][y] = 0
'''
All the attributes given in the DataSet

'Age', 'Attrition', 'BusinessTravel', 'DailyRate', 'Department',
'DistanceFromHome', 'Education', 'EducationField', 'EmployeeCount',
'EmployeeNumber', 'EnvironmentSatisfaction', 'Gender', 'HourlyRate',
'JobInvolvement', 'JobLevel', 'JobRole', 'JobSatisfaction',
'MaritalStatus', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
'Over18', 'OverTime', 'PercentSalaryHike', 'PerformanceRating',
'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
'YearsWithCurrManager'
       
'''

# Drop all the non numerical values, because the RNN works only with numeric values
df.drop(['Attrition', 'Over18', 'StandardHours', 'EmployeeCount', 'EmployeeNumber', 'BusinessTravel', 'Department',
         'Education', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus',
         'OverTime', ], 1, inplace=True)

# Normalising the numerical values, thus changing all the values to common scale and hence increasing the training accuracy

#
min_max_scaler = preprocessing.MinMaxScaler()
keys = df.keys()

df['Age'] = min_max_scaler.fit_transform(df.Age.values.reshape(-1, 1))
df['DailyRate'] = min_max_scaler.fit_transform(df.DailyRate.values.reshape(-1, 1))
df['DistanceFromHome'] = min_max_scaler.fit_transform(df.DistanceFromHome.values.reshape(-1, 1))
df['EnvironmentSatisfaction'] = min_max_scaler.fit_transform(df.EnvironmentSatisfaction.values.reshape(-1, 1))
df['HourlyRate'] = min_max_scaler.fit_transform(df.HourlyRate.values.reshape(-1, 1))
df['JobInvolvement'] = min_max_scaler.fit_transform(df.JobInvolvement.values.reshape(-1, 1))
df['JobLevel'] = min_max_scaler.fit_transform(df.JobLevel.values.reshape(-1, 1))
df['JobSatisfaction'] = min_max_scaler.fit_transform(df.JobSatisfaction.values.reshape(-1, 1))
df['MonthlyIncome'] = min_max_scaler.fit_transform(df.MonthlyIncome.values.reshape(-1, 1))
df['MonthlyRate'] = min_max_scaler.fit_transform(df.MonthlyRate.values.reshape(-1, 1))
df['NumCompaniesWorked'] = min_max_scaler.fit_transform(df.NumCompaniesWorked.values.reshape(-1, 1))
df['PercentSalaryHike'] = min_max_scaler.fit_transform(df.PercentSalaryHike.values.reshape(-1, 1))
df['PerformanceRating'] = min_max_scaler.fit_transform(df.PerformanceRating.values.reshape(-1, 1))
df['RelationshipSatisfaction'] = min_max_scaler.fit_transform(df.RelationshipSatisfaction.values.reshape(-1, 1))
df['StockOptionLevel'] = min_max_scaler.fit_transform(df.StockOptionLevel.values.reshape(-1, 1))
df['TotalWorkingYears'] = min_max_scaler.fit_transform(df.TotalWorkingYears.values.reshape(-1, 1))
df['TrainingTimesLastYear'] = min_max_scaler.fit_transform(df.TrainingTimesLastYear.values.reshape(-1, 1))
df['WorkLifeBalance'] = min_max_scaler.fit_transform(df.WorkLifeBalance.values.reshape(-1, 1))
df['YearsAtCompany'] = min_max_scaler.fit_transform(df.YearsAtCompany.values.reshape(-1, 1))
df['YearsInCurrentRole'] = min_max_scaler.fit_transform(df.YearsInCurrentRole.values.reshape(-1, 1))
df['YearsSinceLastPromotion'] = min_max_scaler.fit_transform(df.YearsSinceLastPromotion.values.reshape(-1, 1))
df['YearsWithCurrManager'] = min_max_scaler.fit_transform(df.YearsWithCurrManager.values.reshape(-1, 1))



amount_of_features = len(df.columns)

data = df.as_matrix()
result = []
for x in data:
    result.append(x)
result = np.array(result)
row = round(0.8 * result.shape[0])

X_train = result[:row]
Y_train = Rtrain.as_matrix()[:row]

X_test = result[row:]
Y_test = Rtrain[row:]

model = Sequential()
model.add(Dense(256, input_dim=amount_of_features, kernel_initializer="uniform", activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(128, kernel_initializer="uniform", activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(1, kernel_initializer="uniform", activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.summary()

model.fit(X_train, Y_train, batch_size=500, epochs=1000, validation_split=0.2, verbose=2)


# Saving
# serialize model to JSON
model_json = model.to_json()
with open("Model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("Model.h5")
print("Saved model to disk")



trainScore = model.evaluate(X_train, Y_train, verbose=0)
print('Train Score: %.5f MSE (%.2f RMSE)' % (trainScore[0], math.sqrt(trainScore[0])))

predict = model.predict(X_test)

reval = []
for val in predict:
    reval.append(round(val[0]))
Y_test = Y_test.as_matrix()

countpre, countreal, rightpre = 0, 0, 0

for x in range(len(reval)):
    pre = int(reval[x])
    real = Y_test[x][0]

    if pre == 1:
        countpre += 1
    if real == 1:
        countreal += 1
    if real == pre == 1:
        rightpre += 1

print(countreal, " ", countpre, " ", rightpre)

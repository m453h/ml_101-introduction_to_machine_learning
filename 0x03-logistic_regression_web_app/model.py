import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class DiabetesPredictor:
	def __init__(self):
		# Load the dataset
		df = pd.read_csv('dataset/01-pima-diabetes.csv')
		self.feature_columns = ['Pregnancies','Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

		# Pre-process the dataset before 
		df[self.feature_columns[1:]] = df[self.feature_columns[1:]].replace(to_replace=0, value=np.nan)
		imputer = SimpleImputer(missing_values=np.nan, strategy='median')
		df_cols = df.columns
		df = imputer.fit_transform(df)
		df = pd.DataFrame(df, columns = df_cols)

		# Get the independent (X) and dependent variables (y)
		X = df[self.feature_columns]
		y = df.Outcome

		# Scale the values of the independent variables
		self.scaler = StandardScaler().fit(X)
		X = self.scaler.transform(X)
		X = pd.DataFrame(X, columns = self.feature_columns)
		
		# Spilt the data into training and test set
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify=df["Outcome"], random_state=24)
		
		# Initialize the model
		self.model = LogisticRegression(random_state=16)
		self.model.fit(X_train,y_train)


	def make_prediction(self, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_fn, age):
		data = {
		'Pregnancies':[pregnancies],
		'Glucose': [glucose],
		'BloodPressure':[blood_pressure],
		'SkinThickness':[skin_thickness],
		'Insulin':[insulin],
		'BMI':[bmi],
		'DiabetesPedigreeFunction':[diabetes_pedigree_fn],
		'Age':[age]
		}

		data = pd.DataFrame(data)
		data = self.scaler.transform(data)
		data = pd.DataFrame(data, columns = self.feature_columns)
		outcome = self.model.predict(data)
		return outcome[0]	
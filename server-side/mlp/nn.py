import numpy as np
import random
import csv
import time
import pickle
from sklearn.model_selection import train_test_split
from sklearn import metrics

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler 


def clean_row(row):
	row = row[1:-3] + [row[-1]]
	out = []
	for i in range(len(row)-1):
		try:
			out.append(float(row[i]))
		except:
			pass
	out.append(int(row[-1]))
	return out

def csv_reader(file_name):
	fields	=	[]
	rows	=	[]
	with open(file_name, 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		fields = next(csvreader)
		for row in csvreader:
			x = clean_row(row)
			# print(x)
			if len(x)==39:
				rows.append(x)

	return fields, rows

h, X = csv_reader("UNSW_NB15_training-set.csv")
# for i in range(2):
# 	print(X[i])
X = np.array(X)
X_train, X_test, y_train, y_test = train_test_split(X[:,:-1], X[:,-1], test_size=0.2, random_state=321)
# for i in range(3):
# 	print(X_train[i])
scaler = StandardScaler()
scaler.fit(X_train) 
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
# for i in range(3):
# 	print(X_train[i]) 
# print(len(X_train), len(y_train))
# print(len(X_test), len(y_test))


clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(32, 16, 2), random_state=1)
clf.fit(X_train, y_train)
filename = 'model.sav'
pickle.dump(clf, open(filename, 'wb'))

start = time.time()
test_pred = clf.predict(X_test)
end = time.time()
print("TIME: " + str(end-start))
print("Accuracy:\t" + str(metrics.accuracy_score(y_test, test_pred)*100) + " %")
conf_met = metrics.confusion_matrix(y_test, test_pred)
print(conf_met)
print(metrics.precision_recall_fscore_support(y_test, test_pred, average='macro'))
print("*****************************************************************************************************")


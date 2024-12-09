
# coding: utf-8

# In[5]:


import sklearn
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
import numpy as np

train_data = np.load('data/training_data.npy', allow_pickle = True)
train_labels = np.load('data/train_labels.npy', allow_pickle = True)
print(train_data.shape, train_labels.shape)

classifier = LogisticRegression(penalty='l2', C=1.0, fit_intercept=False)
classifier.fit(train_data, train_labels) # is the weights, need to pass thru log function
print(classifier.coef_)
 # read in exo data, get scores

 
# Predict probabilities for each pair
pair_probabilities = classifier.predict_proba(train_data)[:, 1]  # Prob that condition 2 > condition 1

# Reconstruct scores for individual control laws
n_laws = int((1 + (1 + 8 * len(train_data))**0.5) / 2)  # Solves N*(N-1)/2 = len(train_data)
scores = np.zeros(n_laws)

# Iterate over training data and aggregate probabilities
pair_idx = 0
for i in range(n_laws):
    for j in range(i + 1, n_laws):
        # Pair i vs j
        scores[i] += 1 - pair_probabilities[pair_idx]  # Prob that law i > law j
        scores[j] += pair_probabilities[pair_idx]      # Prob that law j > law i
        pair_idx += 1

# Rank control laws by scores
ranking = np.argsort(-scores)  # Descending order

# Print results
print("Control Law Scores:", scores)
print("Control Law Ranking:", ranking)

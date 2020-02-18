import numpy as np
from scipy import stats
from pylab import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ### Print Normal Random Variables
# print(stats.norm.rvs(size = 10))
#
# # Create some test data
# dx = .01
# X  = np.arange(-2,2,dx)
# Y  = exp(-X**2)
# # Normalize the data to a proper PDF
# Y /= (dx*Y).sum()
# # Compute the CDF
# CY = np.cumsum(Y*dx)
# # Plot both
# plot(X,Y)
# plot(X,CY,'r--')
# show()
#
# ### Compute the Normal CDF of certain values.
# print(stats.norm.cdf(np.array([1,-1., 0, 1, 3, 4, -2, 6])))
# np.random.seed(282629734)
# # Generate 1000 Student’s T continuous random variables.
# x = stats.t.rvs(10, size=1000)
# # Do some descriptive statistics
# print(x.min())   # equivalent to np.min(x)
# print(x.max())   # equivalent to np.max(x)
# print(x.mean())  # equivalent to np.mean(x)
# print(x.var())   # equivalent to np.var(x))
# stats.describe(x)

# Store the url string that hosts our .csv file
url = "Cartwheeldata.csv"
# Read the .csv file and store it as a pandas Data Frame
df = pd.read_csv(url)
# Create Scatterplot
sns.lmplot(x='Wingspan', y='CWDistance', data=df)
plt.show()

sns.lmplot(x='Wingspan', y='CWDistance', data=df,
           fit_reg=False, # No regression line
           hue='Gender')   # Color by evolution stage
plt.show()

# Construct Cartwheel distance plot
sns.swarmplot(x="Gender", y="CWDistance", data=df)
plt.show()

# Female Boxplot
sns.boxplot(data=df.loc[df['Gender'] == 'F', ["Age", "Height", "Wingspan", "CWDistance", "Score"]])
plt.show()

# Distribution Plot (a.k.a. Histogram)
sns.distplot(df.CWDistance)
plt.show()

# Count Plot (a.k.a. Bar Plot)
sns.countplot(x='Gender', data=df)
plt.xticks(rotation=-45)
plt.show()

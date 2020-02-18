import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
# import statsmodels.api as sm

da = pd.read_csv("myData/nhanes_2015_2016.csv")

# Question 1
# Relabel the marital status variable DMDMARTL to have brief but informative character labels.
# Then construct a frequency table of these values for all people, then for women only, and for men only.
# Then construct these three frequency tables using only people whose age is between 30 and 40.
# print(list(da.columns.values))
# print(da.shape)
da["DMDMARTL"] = da.DMDMARTL.replace({1:"Married", 2:"Widowed", 3:"Divorced", 4:"Separated", 5:"Never married",
6:"Living with partner", 77:"Refused", 99:"Don't Know"})
da["DMDMARTL"] = da.DMDMARTL.fillna("Missing")
da["RIAGENDR"] = da.RIAGENDR.replace({1: "Male", 2: "Female"})
da["RIAGENDR"] = da.RIAGENDR.fillna("Missing")
if False :  # On False step over
    print("Marital freqency table for all Genders \n--------------------------------------\n",
        da["DMDMARTL"].value_counts()/da["DMDMARTL"].count())
    print("\nMarital freqency table for Male only \n------------------------------------\n",
        da[da["RIAGENDR"] == "Male"].DMDMARTL.value_counts() / da[da["RIAGENDR"] == "Male"].DMDMARTL.count())
    print("\nMarital freqency table for Female only \n--------------------------------------\n",
        da[da["RIAGENDR"] == "Female"].DMDMARTL.value_counts() / da[da["RIAGENDR"] == "Female"].DMDMARTL.count())
    print("Marital freqency table Aged between [30, 40)\n--------------------------------------------\n",
        da[(da["RIDAGEYR"] >= 30) & (da["RIDAGEYR"] < 40)].DMDMARTL.value_counts() /
        da[(da["RIDAGEYR"] >= 30) & (da["RIDAGEYR"] < 40)].DMDMARTL.count())


# Question 2
# Restricting to the female population, stratify the subjects into age bands no wider than ten years,
# and construct the distribution of marital status within each age band. Within each age band, present
# the distribution in terms of proportions that must sum to 1.
if False :
    da["agegrp"] = pd.cut(da.RIDAGEYR, [10, 20, 30, 40, 50, 60, 70, 80])# Create age strata based on these cut points
    femaleDa = da[da["RIAGENDR"] == "Female"]
    print(femaleDa.groupby("agegrp")["DMDMARTL"].value_counts() / femaleDa.DMDMARTL.count())

# Question 3
# Construct a histogram of the distribution of heights using the BMXHT variable in the NHANES sample.
if False :
    sns.distplot(da[da["RIAGENDR"] == "Female"].BMXHT.dropna(), kde=False)
    sns.distplot(da[da["RIAGENDR"] == "Male"].BMXHT.dropna(), kde=False).set_title("Hight histogram per Female and Male")
    plt.show()
    sns.boxplot(x = da["BMXHT"].dropna(), y = da["RIAGENDR"]).set_title("Hight boxplot per Female and Male")
    g = sns.FacetGrid(da, row = "RIAGENDR")
    g = g.map(plt.hist, "BMXHT")
    plt.show()

# Question 4
# Make a boxplot showing the distribution of within-subject differences between the first
# and second systolic blood pressure measurents (BPXSY1 and BPXSY2).
sns.boxplot(x = da.BPXSY2 - da.BPXSY1, y = da.RIAGENDR.dropna()).set_title("Differences between the first and second systolic blood pressure")
sys.exit()

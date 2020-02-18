import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

da = pd.read_csv("nhanes_2015_2016.csv")

da.DMDEDUC2.value_counts()

# Note that the value_counts method excludes missing values. We confirm this below by adding up
# the number of observations with a DMDEDUC2 value equal to 1, 2, 3, 4, 5, or 9 (there are 5474 such rows),
# and comparing this to the total number of rows in the data set, which is 5735.
# This tells us that there are 5735 - 5474 = 261 missing values for this variable (other variables may have different numbers of missing values).
print(da.DMDEDUC2.value_counts().sum())
print(1621 + 1366 + 1186 + 655 + 643 + 3) # Manually sum the frequencies
print(da.shape)

# Another way to obtain this result is to locate all the null (missing) values in the data set
# using the isnull Pandas function, and count the number of such locations.
pd.isnull(da.DMDEDUC2).sum()

# In some cases it is useful to replace integer codes with a text label that reflects
# the code's meaning.  Below we create a new variable called 'DMDEDUC2x' that is recoded
# with text labels, then we generate its frequency distribution.
da["DMDEDUC2x"] = da.DMDEDUC2.replace({1: "<9", 2: "9-11", 3: "HS/GED", 4: "Some college/AA", 5: "College",
                                       7: "Refused", 9: "Don't know"})
da.DMDEDUC2x.value_counts()

# We will also want to have a relabeled version of the gender variable, so we will construct
# that now as well.  We will follow a convention here of appending an 'x' to the end of a
# categorical variable's name when it has been recoded from numeric to string (text) values.
da["RIAGENDRx"] = da.RIAGENDR.replace({1: "Male", 2: "Female"})
print(da.RIAGENDRx.value_counts())
print(da.RIAGENDR.value_counts())

# For many purposes it is more relevant to consider the proportion of the sample with
# each of the possible category values, rather than the number of people in each category.  We can do this as follows:
x = da.DMDEDUC2x.value_counts()  # x is just a name to hold this value temporarily
x / x.sum()

# In some cases we will want to treat the missing response category as another category of observed response,
# rather than ignoring it when creating summaries.  Below we create a new category called "Missing",
# and assign all missing values to it usig fillna
# Then we recalculate the frequency distribution.  We see that 4.6% of the responses are missing.
da["DMDEDUC2x"] = da.DMDEDUC2x.fillna("Missing")
x = da.DMDEDUC2x.value_counts()
x / x.sum()

# A quick way to get a set of numerical summaries for a quantitative variable is with the [describe]
# As with many surveys, some data values are missing, so we explicitly drop the missing cases
# using the dropna method before generating the summaries.
da.BMXWT.dropna().describe()

# It's also possible to calculate individual summary statistics from one column of a data set.
# This can be done using Pandas methods, or with numpy functions:
x = da.BMXWT.dropna()  # Extract all non-missing values of BMXWT into a variable called 'x'
print(x.mean()) # Pandas method
print(np.mean(x)) # Numpy function

print(x.median())
print(np.percentile(x, 50))  # 50th percentile, same as the median
print(np.percentile(x, 75))  # 75th percentile
print(x.quantile(0.75)) # Pandas method for quantiles, equivalent to 75th percentile

# Next we look at frequencies for a systolic blood pressure measurement ([BPXSY1]
# "BPX" here is the NHANES prefix for blood pressure measurements, "SY" stands for "systolic"
# blood pressure (blood pressure at the peak of a heartbeat cycle), and "1" indicates that this is
# the first of three systolic blood presure measurements taken on a subject.
# A person is generally considered to have pre-hypertension when their systolic blood pressure is
# between 120 and 139, or their diastolic blood pressure is between 80 and 89.  Considering only the
# systolic condition, we can calculate the proprotion of the NHANES sample who would be considered
# to have pre-hypertension.
np.mean((da.BPXSY1 >= 120) & (da.BPXSY2 <= 139))  # "&" means "and"

# Finally we calculate the proportion of NHANES subjects who are pre-hypertensive based on either
# systolic or diastolic blood pressure. Since some people are pre-hypertensive under both criteria,
# the proportion below is less than the sum of the two proportions calculated above.
# Since the combined systolic and diastolic condition for pre-hypertension is somewhat complex,
# below we construct temporary variables 'a' and 'b' that hold the systolic and diastolic
# pre-hypertensive status separately, then combine them with a "logical or" to obtain the final
# status for each subject.
a = (da.BPXSY1 >= 120) & (da.BPXSY2 <= 139)
b = (da.BPXDI1 >= 80) & (da.BPXDI2 <= 89)
print(np.mean(a), b.mean())
print(np.mean(a | b))  # "|" means "or"

# Blood pressure measurements are affected by a phenomenon called "white coat anxiety", in which
# a subject's bood pressure may be slightly elevated if they are nervous when interacting with
# health care providers.  Typically this effect subsides if the blood pressure is measured several
# times in sequence.  In NHANES, both systolic and diastolic blood pressure are meausred three times
# for each subject (e.g. [BPXSY2](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.htm#BPXSY2) is the second measurement of systolic blood pressure).  We can calculate the extent to which white coat anxiety is present in the NHANES data by looking a the mean difference between the first two systolic or diastolic blood pressure measurements.
print(np.mean(da.BPXSY1 - da.BPXSY2))
print(np.mean(da.BPXDI1 - da.BPXDI2))

# Quantitative variables can be effectively summarized graphically.  Below we see the distribution
# of body weight (in Kg), shown as a histogram.  It is evidently right-skewed.
sns.distplot(da.BMXWT.dropna(), kde=True).set_title("Malakies")
print("mean : ", np.mean(da.BMXWT.dropna()))
print(da.BMXWT.dropna().describe())

# Next we look at the histogram of systolic blood pressure measurements.  You can see that
# there is a tendency for the measurements to be rounded to the nearest 5 or 10 units.
sns.distplot(da.BPXSY1.dropna())

# To compare several distributions, we can use side-by-side boxplots.  Below we compare the
# distributions of the first and second systolic blood pressure measurements (BPXSY1, BPXSY2),
# and the first and second diastolic blood pressure measurements ([BPXDI1] BPXDI2). As expected, diastolic measurements
# are substantially lower than systolic measurements.  Above we saw that the second blood
# pressure reading on a subject tended on average to be slightly lower than the first measurement.
# This difference was less than 1 mm/Hg, so is not visible in the "marginal" distributions shown below.
bp = sns.boxplot(da.loc[:, ["BPXSY1", "BPXSY2", "BPXDI1", "BPXDI2"]])
_ = bp.set_ylabel("Blood pressure in mm/Hg")

### Stratification
# One of the most effective ways to get more information out of a dataset is to divide it into smaller,
# more uniform subsets, and analyze each of these "strata" on its own.  We can then formally or
# informally compare the findings in the different strata.  When working with human subjects, it is
# very common to stratify on demographic factors such as age, sex, and race.
# To illustrate this technique, consider blood pressure, which is a value that tends to increase with age.
# To see this trend in the NHANES data, we can [partition] the data into age strata, and construct side-by-side boxplots
# of the systolic blood pressure (SBP) distribution within each stratum.  Since age is a
# quantitative variable, we need to create a series of "bins" of similar SBP values in order to stratify the data.
# Each box in the figure below is a summary of univariate data within a specific population
# stratum (here defined by age).
da["agegrp"] = pd.cut(da.RIDAGEYR, [18, 30, 40, 50, 60, 70, 80]) # Create age strata based on these cut points
plt.figure(figsize=(12, 5))  # Make the figure wider than default (12cm wide by 5cm tall)
sns.boxplot(x="agegrp", y="BPXSY1", data=da)  # Make boxplot of BPXSY1 stratified by age group

# Taking this a step further, it is also the case that blood pressure tends to differ between women and men.
# While we could simply make two side-by-side boxplots to illustrate this contrast, it would be a bit
# odd to ignore age after already having established that it is strongly associated with blood pressure.
# Therefore, we will doubly stratify the data by gender and age.
# We see from the figure below that within each gender, older people tend to have higher blood pressure
# than younger people.  However within an age band, the relationship between gender and systolic blood
# pressure is somewhat complex -- in younger people, men have substantially higher blood pressures than
# women of the same age.  However for people older than 50, this relationship becomes much weaker, and
# among people older than 70 it appears to reverse. It is also notable that the variation of these
# distributions, reflected in the height of each box in the boxplot, increases with age.
da["agegrp"] = pd.cut(da.RIDAGEYR, [18, 30, 40, 50, 60, 70, 80])
plt.figure(figsize=(12, 5))
sns.boxplot(x="agegrp", y="BPXSY1", hue="RIAGENDRx", data=da)

# When stratifying on two factors (here age and gender), we can group the boxes first by age,
# and within age bands by gender, as above, or we can do the opposite -- group first by gender,
# and then within gender group by age bands.  Each approach highlights a different aspect of the data.
da["agegrp"] = pd.cut(da.RIDAGEYR, [18, 30, 40, 50, 60, 70, 80])
plt.figure(figsize=(12, 5))
sns.boxplot(x="RIAGENDRx", y="BPXSY1", hue="agegrp", data=da)

# Stratification can also be useful when working with categorical variables.  Below we look at the
# frequency distribution of educational attainment ("DMDEDUC2") within 10-year age bands.
# While "some college" is the most common response in all age bands, up to around age 60 the second
# most common response is "college" (i.e. the person graduated from college with a four-year degree).
# However for people over 50, there are as many or more people with only high school or general
# equivalency diplomas (HS/GED) than there are college graduates.
da.groupby("agegrp")["DMDEDUC2x"].value_counts()

# We can also stratify jointly by age and gender to explore how educational attainment varies by
# both of these factors simultaneously.  In doing this, it is easier to interpret the results if we
# [pivot] reshaping-by-stacking-and-unstacking) the education levels into the columns, and normalize
# the counts so that they sum to 1.  After doing this, the results can be interpreted as proportions or
# probabilities.  One notable observation from this table is that for people up to age around 60,
# women are more likely to have graduated from college than men, but for people over aged 60, this
# relationship reverses.
dx = da.loc[~da.DMDEDUC2x.isin(["Don't know", "Missing"]), :]  # Eliminate rare/missing values
dx = dx.groupby(["agegrp", "RIAGENDRx"])["DMDEDUC2x"]
dx = dx.value_counts()
dx = dx.unstack() # Restructure the results from 'long' to 'wide'
dx = dx.apply(lambda x: x/x.sum(), axis=1) # Normalize within each stratum to get proportions
print(dx.to_string(float_format="%.3f"))  # Limit display to 3 decimal places

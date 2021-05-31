import pandas as pd

# load the dataset
df = pd.read_csv('digital_product_sales.csv')
# the dataset
# PRICE     the sale price of the product (int64)
# SOURCE    the source of the sale (object)
# SEX       the gender of the customer (object)
# COUNTRY   the country of the customer (object)
# AGE       the age of the customer (int64)

# describe the data
print(df.shape)
print(df.head())
print(df.info())
print(df.describe())

# class names and frequencies of the SOURCE categorical variable
df["SOURCE"].value_counts()

# the number of sales for each PRICE
df["PRICE"].value_counts()

# the number of sales from each COUNTRY
df["COUNTRY"].value_counts()

# total revenue of sales from each COUNTRY
df.groupby("COUNTRY").agg({"PRICE": "sum"})

# the number of sales from each SOURCE
df["SOURCE"].value_counts()

# average revenue of sales from each COUNTRY
df.groupby("COUNTRY").agg({"PRICE": "mean"})

# average revenue of sales from each SOURCE
df.groupby("SOURCE").agg({"PRICE": "mean"})

# average revenue of sales by COUNTRY and SOURCE sub-groups
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

# total revenue of sales by COUNTRY, SOURCE, SEX and AGE sub-groups
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "sum"})

# descending order of total revenue of sales by COUNTRY, SOURCE, SEX and AGE sub-groups
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "sum"}).sort_values("PRICE", ascending=False)
agg_df.head()

# reset MultiIndex DataFrame to DataFrame with RangeIndex
# agg_df is a MultiIndex dataframe, we will reset index now and MultiIndex will become 4 new columns
agg_df = agg_df.reset_index()
agg_df.head()

# convert AGE variable to a categorical variable divided into labeled bins
# you can define different scale bins for age variable
bins = [0, 15, 20, 30, 40, 60, 80]
labels = ["0_15", "16_20", "21_30", "31_40", "41_60", "61_80"]
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins = bins, labels = labels)
# let's see the frequencies of age categories (AGE_CAT)
agg_df["AGE_CAT"].value_counts()
agg_df.head()

# Define personas in LEVEL_BASED_PERSONAS variable
agg_df["LEVEL_BASED_PERSONAS"] = agg_df.apply(lambda row: row["COUNTRY"].upper() + "_" + row["SOURCE"].upper() + "_" + row["SEX"].upper() + "_" + row["AGE_CAT"].upper(), axis=1)
agg_df.drop(["COUNTRY", "SOURCE", "SEX", "AGE", "AGE_CAT"], axis=1, inplace=True)
agg_df.head()

# groupby LEVEL_BASED_PERSONAS for one-to-one relation
agg_df = agg_df.groupby("LEVEL_BASED_PERSONAS").agg({"PRICE": "mean"})
# reset index
agg_df = agg_df.reset_index()
agg_df.head()

# Divide personas into 4 equal segments A, B, C, D
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head()

# predict possible revenue and segment of a new customer
# new customer 1: Which segment includes a 39-year-old German woman using ANDROID what is the expected average revenue from this segment?
# new customer 2: Which segment includes a 19-year-old French woman using iOS what is the expected average revenue from this segment?
new_cust1 = "DEU_ANDROID_FEMALE_31_40"
new_cust2 = "FRA_IOS_FEMALE_16_20"
# customer below is absent in our historical data
#new_cust2 = "FRA_IOS_FEMALE_41_60"

revenue1, revenue2 = (0,0)
segment1, segment2 = ("", "")

# let's check if there is a segment in our historical data we can include new customers.
if len(agg_df[agg_df["LEVEL_BASED_PERSONAS"] == new_cust1]) > 0 :
    revenue1 = agg_df[agg_df["LEVEL_BASED_PERSONAS"] == new_cust1]["PRICE"].values[0]
    segment1 = agg_df[agg_df["LEVEL_BASED_PERSONAS"] == new_cust1]["SEGMENT"].values[0]

if len(agg_df[agg_df["LEVEL_BASED_PERSONAS"] == new_cust2]) > 0 :
    revenue2 = agg_df[agg_df["LEVEL_BASED_PERSONAS"] == new_cust2]["PRICE"].values[0]
    segment2 = agg_df[agg_df["LEVEL_BASED_PERSONAS"] == new_cust2]["SEGMENT"].values[0]

# print new customers' segments and possible revenues from these segments
print(f"{new_cust1} >> revenue: {revenue1} segment: {segment1}" if revenue1 > 0 else f"{new_cust1} >> customer level unidentified!")
print(f"{new_cust2} >> revenue: {revenue2} segment: {segment2}" if revenue2 > 0 else f"{new_cust2} >> customer level unidentified!")
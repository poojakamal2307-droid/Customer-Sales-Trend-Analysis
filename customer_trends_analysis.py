import pandas as pd
df = pd.read_csv(r"D:\customer_shopping_behavior.csv")

df.head()
print(df.head())

print(df.info())
#summary statistics using .describe()

print(df.describe(include='all'))

#checking if missing data or null values are present in the dataset

print(df.isnull().sum())

#Imputing missing values in Review Rating column with the median rating of the product category


df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

# Renaming columns according to snake casing for better readability and documentation

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

print(df.columns)

#create a new column age_group

labels = ['young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)

print(df[['age', 'age_group']].head(10))

#create new column purchase_frequency_days

frequency_mapping = {
    'Fortnightly' : 14,
    'Weekly' : 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10))

print(df[['discount_applied','promo_code_used']].head(10))

print((df['discount_applied'] == df['promo_code_used']).all())

#Dropping promo code used column

df = df.drop('promo_code_used', axis=1)
print(df.columns)


from sqlalchemy import create_engine
from urllib.parse import quote_plus

host = "localhost"
username = "root"
password = quote_plus("Root@1234")   # encode special characters
database = "customer_behavior_db"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}"
)

table_name = "customer"


df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")

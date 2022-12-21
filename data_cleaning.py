import pandas as pd
import math

df = pd.read_csv('data scientist.csv')

# salary parsing
df['hourly'] = df['salary estimate'].apply(lambda x: 1 if '/hr' in x.lower() else 0)
df['monthly'] = df['salary estimate'].apply(lambda x: 1 if '/mo' in x.lower() else 0)


df = df[df['salary estimate'] != "-1"]
salary = df['salary estimate'].apply(lambda x: x.split("(")[0])
minus_Kd = salary.apply(lambda x: x.replace("$", "").replace("₹", ""))
min_time = minus_Kd.apply(lambda x: x.lower().replace("/hr", "").replace("/yr", "").replace("/mo", ""))
# Company name text only
df['company_txt'] = df['company'].apply(lambda x: x.split("\n")[0])
# count of locations
df.location.value_counts()
# age of company

df['age'] = df['company_founded'].apply(lambda x: x if x < 1 else 2022 - x)

# parsing of job description (python, etc.)

#python
df['python_yn'] = df['job description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()
#r stuido
df['R_yn'] = df['job description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()
#spark
df['spark'] = df['job description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()
#aws
df['aws'] = df['job description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()
#excel
df['excel'] = df['job description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

df_out = df.drop('Unnamed: 0', axis=1)

df_out.to_csv('salary_data_cleaning.csv', index=False)

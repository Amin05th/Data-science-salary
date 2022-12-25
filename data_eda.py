import nltk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
pd.set_option('display.max_rows', None)
df = pd.read_csv('salary_data_cleaning.csv')

def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'machine learning' in title.lower():
        return 'machine learning'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'


def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'


# Job title and seniority
df['job_simp'] = df['job title'].apply(title_simplifier)
df.job_simp.value_counts()

df['seniority'] = df['job title'].apply(seniority)
df.seniority.value_counts()
# Job description length

df['desc_len'] = df['job description'].apply(lambda x: len(x))

# hourly wage to annual

df['salary'] = df.apply(lambda x: x['salary']*2 if x.hourly == 1 else x['salary'], axis=1)

# monthly wage to annual

df['salary'] = df.apply(lambda x: x['salary']*12 if x.monthly == 1 else x['salary'], axis=1)

df.age.hist()
df.salary.hist()
df.desc_len.hist()
df.boxplot(column='age')

corr = df[['age', 'desc_len', 'salary']].corr()
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=cmap, vmax=3, center=0, square=True, linewidths=5, cbar_kws={"shrink": .5})
plt.show()

df_cat = df[['location', 'company_size', 'company_type', 'company_industry', 'company_sector', 'company_revenue',
    'python_yn', 'R_yn', 'spark', 'aws', 'excel', 'job_simp', 'seniority']]

for i in df_cat.columns:
    cat_num = df_cat[i].value_counts()
    # print("graph for %s: total = %d" % (i, len(cat_num)))
    chart = sns.barplot(x=cat_num.index, y=cat_num)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90)
    plt.show()


pd.pivot_table(df, index=["job_simp", 'seniority'], values="salary")
pd.pivot_table(df, index=['location', 'job_simp'], values="salary", aggfunc="count").sort_values('location', ascending=False)
pd.pivot_table(df[df.job_simp == "data scientist"], index='location', values="salary").sort_values('salary', ascending=False)

# industry, sector, revenue, number of comp, hourly, python, r, spark, aws, excel, desc_len, type of owenership

df_pivots = df[['company_industry', 'company_sector', 'company_revenue', 'hourly', 'monthly', 'python_yn', 'R_yn',
           'spark', 'aws', 'excel', 'salary']]

for i in df_pivots.columns:
    pd.pivot_table(df_pivots, index=i, values="salary").sort_values('salary', ascending=False)
    pass

pd.pivot_table(df_pivots, index='company_revenue', columns="python_yn", values="salary", aggfunc="count")


words = " ".join(df['job description'])


def punctuation_stop(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    return [w.lower() for w in word_tokens if w not in stop_words and w.isalpha()]


words_filtered = punctuation_stop(words)

text = " ".join(list(words_filtered))

wc = WordCloud(background_color="white", random_state=1, stopwords=STOPWORDS, max_words=2000, width=800, height = 1500)
wc.generate(text)

plt.figure(figsize=[10, 10])
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.show()

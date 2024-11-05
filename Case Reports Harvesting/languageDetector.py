from langdetect import detect
import pandas as pd


df=pd.read_csv("dataset_articles.csv")



languages=list()



for index,row in df.iterrows():
    l=detect(row["articles"])
    languages.append(l)


df["language"]=languages
df.to_csv("dataset_articles.csv",index=None)


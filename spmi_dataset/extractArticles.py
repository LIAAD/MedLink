

import requests
from bs4 import BeautifulSoup



def extractArticle(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  elements = soup.find_all(class_="text14")
  text_content=list()
  for element in elements:

    # Extract text from each <p> within the element and join with newlines
    paragraphs = element.find_all(['p','img'])
    if paragraphs:
      text=""
      for p in paragraphs:
        if p.name=="p":
        # Extract text from each <p> and join with newlines
          text = text + p.get_text() + "\n"
        elif p.name=="img":
          text = text + p.get("src") + "\n"
    else:
      # If no <p> elements, extract the entire text content
        text = element.get_text()

    text_content.append(text)
  return(text_content)


def convertElements2Struct(link,text_content):
  article=dict()
  article.update({"link":link})
  article.update({"title":text_content[0]})
  article.update({"journal":text_content[1]})
  article.update({"category":text_content[2]})
  article.update({"authors":text_content[4]})
  article.update({"affiliations":text_content[6]})
  article.update({"acceptance Date":text_content[8]})
  article.update({"publication Date":text_content[10]})
  article.update({"ISSN":text_content[12]})
  article.update({"abstract":text_content[14]})
  article.update({"keywords":text_content[16]})
  article.update({"articles":text_content[18]})
  return article

import pandas as pd
import time
import random

if __name__ == '__main__':

  results=[]
  links=pd.read_csv("linksSPMI.csv")
  links=set(list(links["source"]))
  for link in list(links)[0:1]:
      print(link)
      time.sleep(random.randint(3, 7))
      try:
        article = extractArticle(link)
        print(article)
        print("article extracted")
        structure = convertElements2Struct(link,article)
        print("elements stuctured")

        results.append(structure)
        print(structure)
      except Exception as e:
        print("Problems: " + str(e))


  df_results=pd.DataFrame.from_dict(results)

  print(df_results)
  #df_results.to_csv("datasets_articles.csv")
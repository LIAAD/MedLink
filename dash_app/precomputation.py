from transformers import pipeline

from transformers import pipeline

import spacy
ner_health_pipeline = pipeline('ner', model='portugueseNLP/medialbertina_pt-pt_900m_NER', aggregation_strategy='average')
ner_spacy = spacy.load("pt_core_news_sm")


def computeHealthNER(text):
    doc=ner_spacy(text)
    sentences = [sent.text for sent in doc.sents]

    entities=list()
    for sentence in sentences:
        sent_ent = ner_health_pipeline(sentence)
        entities.append({"sentence":sentence,"entities":sent_ent})
    return entities








def precomputeNER(df):
    precomputed_entities=list()
    for ind,row in df.iterrows():
        print(row["abstract"])
        try:
            temp=computeHealthNER(row["abstract"])
            print(temp)
            precomputed_entities.append({
                "id":row["Unnamed: 0"],
                "entities":temp
            })
        except Exception as e:
            print(str(e))
            precomputed_entities.append({
                "id": row["Unnamed: 0"],
                "entities": []
            })
    return precomputed_entities





"""
import pandas as pd


from unidecode import unidecode
df=pd.read_csv("dataset_articles_2.csv")

def preprocess_keywords(keywords):
    if pd.isnull(keywords):
        return []
    black_list = ["efeitos adversos", "diagnóstico por imagem", "complicações", "diagnóstico", "portugal","cultura"]
    words = keywords.lower().replace(';', ',').replace('/', ',').split(',')
    words = [word.strip() for word in words]
    words = [word.strip(".,") for word in words]
    words = [word for word in words if len(word) > 2 and word not in  black_list]
    words = [unidecode(word) for word in words]
    return words

#uniformizar keywords
df['processed_keywords'] = df['keywords'].apply(preprocess_keywords)
filtered_df = df[df['processed_keywords'].apply(len) > 0]
filtered_df = df[df['abstract'].str.len() > 40]
#remove abstracts with "Imagens em Medicina - Sem resumo"
filtered_df = filtered_df[filtered_df['abstract'] != "Imagens em Medicina - Sem resumo"]
filtered_df = filtered_df[filtered_df['abstract'] != "Não aplicável - Imagens em Medicina"]

filtered_df = filtered_df[filtered_df['abstract'] != "Imagens em Medicina - Sem necessidade de resumo, de acordo com informações"]
#print datafram count
filtered_df.shape

filtered_df.to_csv("filtered_df.csv")



text='''Paciente feminina, 84 anos, com queixas de fadiga, mialgias, fraqueza muscular generalizada e disfagia há 2 semanas. Ao exame, tetraparésia proximal com hiporreflexia, sensibilidade preservada. Analiticamente, padrão inflamatório com hipercalcemia, elevação das aminotransferases e rabdomiólise. Hipogamaglobulinemia com hepatite e esofagite por reativação viral.

Suspeita de síndrome paraneoplásico associado a timoma. A aguardar TC torácica e investigação complementar.'''
import pandas as pd

"""
import pandas as pd

df=pd.read_csv("filtered_df.csv")

result=precomputeNER(df)



for r in result:
    for sent in r["entities"]:
        for ent in sent["entities"]:
            ent["score"]=str(ent["score"])
            ent["start"] = str(ent["start"])
            ent["end"] = str(ent["end"])



import json
with open("entities_data.json", "w") as json_file:
    json.dump(result, json_file, indent=4)

print("JSON file saved successfully!")


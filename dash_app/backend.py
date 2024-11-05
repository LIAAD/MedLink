import json

import pandas as pd
import os
from dash import html, dcc,callback, page_container,page_registry

from gensim.models import Word2Vec
import dash_bootstrap_components as dbc
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import tokenize

from gensim.utils import tokenize
import numpy as np
import json
stop_words = stopwords.words('portuguese')
global df
current_directory = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(current_directory,"filtered_df.csv"))
entities_df=json.load(open(os.path.join(current_directory,"entities_data.json")))
from transformers import pipeline

import spacy
ner_health_pipeline = pipeline('ner', model='portugueseNLP/medialbertina_pt-pt_900m_NER', aggregation_strategy='average',device=0)
ner_spacy = spacy.load("pt_core_news_sm")


 #test the model on inference given a an abstract and the list of abstracts
from sentence_transformers import SentenceTransformer, util, CrossEncoder
import torch
cross_model = CrossEncoder("lfcc/medlink-cross-encoder", num_labels=1, max_length=512)
# Load the model
model_bi_encoder = SentenceTransformer("lfcc/medlink-bi-encoder")

#Calculate the abstract embeddings - This only need to be done once


def loadModelsandData_update():



    embeddings = model_bi_encoder.encode(df["abstract"].tolist(), convert_to_tensor=True)

    return df,embeddings


import re

def getDocumentCandidates(query_text,abstracts,embeddings):
    #query_text = re.sub(r'\s+', ' ', query_text)
    # Strip leading and trailing spaces
    #query_text = query_text.strip()

    query_embedding = model_bi_encoder.encode(query_text, convert_to_tensor=True)
    #print("_____________________________-")
    #print(abstracts)
    # Calculate the similarity between the query and the abstracts
    cosine_scores = util.pytorch_cos_sim(query_embedding, embeddings)
    retrieval_results = torch.topk(cosine_scores, k=10)
    #print("_____________________________")
    #print(retrieval_results)
    #print("______________________________")
    retrieved_abstracts = [abstracts[idx] for idx in retrieval_results.indices[0]]
    reranking_results = cross_model.rank(query_text, retrieved_abstracts)


    reranked_abstracts = []

    for rank in reranking_results:
        retrieval_idx = rank['corpus_id']
        # print(retrieval_results.indices[0][retrieval_idx])
        abstract_idx = retrieval_results.indices[0][retrieval_idx].cpu().numpy()
        # add score to
        # get entries from the filtered_df
        paper = df.iloc[abstract_idx].copy()
        paper['score'] = rank['score']
        reranked_abstracts.append(paper)
    return reranked_abstracts









def computeHealthNER(text):
    doc=ner_spacy(text)
    sentences = [sent.text for sent in doc.sents]

    entities=list()
    for sentence in sentences:
        sent_ent = ner_health_pipeline(sentence)
        entities.append({"sentence":sentence,"entities":sent_ent})
    return entities






def get_mean_vector(text,model):
    vectors = [model.wv[token] for token in tokenize(text, lower=True) if token not in stop_words and token in model.wv]
    mean = np.mean(vectors, axis = 0)
    return mean


def cosine(v1, v2):
    return np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

"""
def loadModelsandData():

    abstracts = [a for a in df["abstract"] if
                 type(a) == str and len(a) > 30 and "Não necessita resumo" not in a and "Não aplicável " not in a]

    model = Word2Vec.load(os.path.join("models","ata_medica.w2v"))
    return abstracts,model

"""


def extractArticles(ref_text,abstracts,model):

    sims = []
    query_vector = get_mean_vector(ref_text,model)
    for i, text in enumerate(abstracts):
        title_vector =  get_mean_vector(text,model)
        sim = cosine(query_vector,title_vector)
        sims.append((i,sim))

    sorted_sims = sorted(sims,key=lambda x : x[1], reverse=True)
    return sorted_sims
    #for i, sim in sorted_sims[:10]:
    #    print(sim, abstracts[i])

def mapArticles(list_matches):
    list_results=list()
    for (ind,conf) in list_matches:
        di_temp=dict()
        entry_df=df.iloc[ind]
        di_temp["id"]=ind
        di_temp["conf"]=conf
        di_temp["link"]=entry_df["link"]
        di_temp["title"]=entry_df["title"]
        di_temp["abstract"]=entry_df["abstract"]
        list_results.append(di_temp)

    return list_results


def getArticleMetadata(article_id):
    entry=df[df["Unnamed: 0.1"] == int(article_id)]
    return entry



entity_colors = {
    "Diagnostico": "#F09EA7",
    "Sintoma": "#F6CA94",
    "Medicamento": "#FAFABE",
    "Dosagem": "#C1EBC0",
    "ProcedimentoMedico": "#C7CAFF",
    "SinalVital": "#CDABEB",
    "Progresso": "#F6C2F3",
    "Resultado": "#8EA1F0"
}

name_corrections = {
    "Diagnostico": "Diagnóstico",
    "ProcedimentoMedico": "Procedimento Médico",
    "SinalVital": "Sinal Vital",
}




def highlight_entities(text, entities):
    # Sort entities by start index in reverse order so we can replace the text without messing up the indexes by adding characters to the text
    entities_sorted = sorted(entities, key=lambda e: int(e['start']), reverse=True)
    for entity in entities_sorted:
        start, end = int(entity["start"]) + 1, int(entity["end"])
        word = text[start:end]
        color = entity_colors.get(entity["entity_group"], "lightgrey")
        highlighted_word = f'<span style="background-color: {color}; font-weight: bold;">{word}</span>'
        text = text[:start] + highlighted_word + text[end:]
    return text

def mapEntities(article_id):
    entry=[e for e in entities_df if e["id"]==article_id][0]

    text=""
    for sent in entry["entities"]:
        text=text+" "+highlight_entities(sent["sentence"],sent["entities"])
    return text



def mapEntitiesText(entry):
    text=""
    for sent in entry:
        text=text+" "+highlight_entities(sent["sentence"],sent["entities"])
    return text

def generate_legend():
    legend_items = []
    for entity, color in entity_colors.items():
        if entity in name_corrections.keys():
            entity=name_corrections[entity]
        legend_items.append(
            dbc.Row([
                dbc.Col(html.Div(style={"backgroundColor": color, "width": "4vh", "height": "4vh"})),
                dbc.Col(html.Span(entity), align="left")
            ], align="center")
        )
    return legend_items






'''
from transformers import TRANSFORMERS_CACHE
import torch
import shutil
import os
import csv
from tqdm import tqdm

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Specify the LLM model we'll be using
model_gen_name = "microsoft/Phi-3-mini-4k-instruct"

# Configure for GPU usage
model_gen = AutoModelForCausalLM.from_pretrained(
    model_gen_name,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True,
)

# Load the tokenizer for the chosen model
tokenizer_gen = AutoTokenizer.from_pretrained(model_gen_name)

# Create a pipeline object for easy text generation with the LLM
pipe_text_gen = pipeline("text-generation", model=model_gen, tokenizer=tokenizer_gen)

generation_args = {
    "max_new_tokens": 512,     # Maximum length of the response -> maybe change to 100 (summary must have 80 words maximum)
    "return_full_text": False,      # Only return the generated text
}
def query(messages):
  """Sends a conversation history to the AI assistant and returns the answer.

  Args:
      messages (list): A list of dictionaries, each with "role" and "content" keys.

  Returns:
      str: The answer from the AI assistant.
  """
  output = pipe_text_gen(messages, truncation=True, **generation_args)
  return output[0]['generated_text']

def generate_explanation(clinical_narrative,abstract):
  context="""
  Fazes parte de uma ferramenta de apoio à decisão em hospitais que permite consultar um histórico de casos clínicos de diferentes pacientes para ajudar a tomar melhores decisões com um novo paciente.
  O teu objetivo é analisar e relatar a semelhança entre a narrativa clinica de um paciente atual e um resumo que relata um caso clínico préviamente identificado.
  O texto deverá ser sucinto e explicativo. Deverá conter apenas nas semelhanças dos dois textos e ser escrito em português.
  """

  print("generating explanation")
  messages = [
      {"role": "system",
       "content": context },
      {"role": "user",
       "content": f'narrativa clínica: {clinical_narrative} \n caso clínico: {abstract}' '\n Resultado:'}
  ]
  result = query(messages)
  print(result)
  return result
'''

import vertexai
from vertexai.generative_models import GenerativeModel

# TODO(developer): Update and un-comment below line
# PROJECT_ID = "your-project-id"
vertexai.init(project="medsearch-439514", location="us-central1")

model_gemini = GenerativeModel("gemini-1.5-flash-002")


import time
def generate_explanation(clinical_narrative,abstract):
  #time.sleep(3)
  context="""
  Fazes parte de uma ferramenta de apoio à decisão em hospitais que permite consultar um histórico de casos clínicos de diferentes pacientes para ajudar a tomar melhores decisões com um novo paciente.
  O teu objetivo é analisar e relatar a semelhança entre a narrativa clinica de um paciente atual e um resumo que relata um caso clínico préviamente identificado.
  O texto deverá ser sucinto e explicativo. Deverá conter apenas nas semelhanças dos dois textos e ser escrito em português.
  """
  print(context + "\n" + f'narrativa clínica: {clinical_narrative} \n caso clínico: {abstract}' '\n Resultado:')
  response = model_gemini.generate_content(
     context + "\n" + f'narrativa clínica: {clinical_narrative} \n caso clínico: {abstract}' '\n Resultado:'
  )
  return response.text
  #print(response.text)
  return '''Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.
   Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.
   Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo.
   
   Exemplo de texto explicativo.Exemplo de texto explicativo.Exemplo de texto explicativo. Exemplo de texto explicativo.'''
from pypdf import PdfReader # used to read pdf
from sentence_transformers import SentenceTransformer #create vectors
import chromadb #use to connect to vectordb
from openai import OpenAI #used to generate output

import os

model = SentenceTransformer("all-MiniLM-L6-v2") #load the model
client=chromadb.Client() #create the table 
collection = client.create_collection("pdf_data")

#Reading Pdf File
def read_pdf(pdf_path):
    reader=PdfReader(pdf_path)
    text=""

    for page in reader.pages:
        extracted_text=page.extracted_text()
        if extracted_text:
            text+= extracted_text

    return text

#chuncking

def chunck_text(text):
    chunck_size = 500
    chuncks=[]

    for i in range(0,len(text).chunck_size):
        chunck=text[i:i+chunck_size]
        chuncks.append(chunck)

    return chuncks

#Embeddings

def create_embeddings(chuncks):
    embeddings=model.encode(chuncks)
    return embeddings

#store in chromadb

def store_in_chromadb(chuncks,embeddings):
    collection.add(documents=chuncks,embeddings=embeddings.tolist(),ids=[str(i)for i in range(len(chuncks))])
    return "Data stored succesfully!!"


#search

def search_query(question):
    query_embedding=model.encode([question])

    results=collection.query(query_embeddings=query_embedding.tolist(),n_result=2)
    return results

#generate output

def generate_answer(question,context):
    api_key = os.getenv("api_key")
    openai_client=OpenAI(api_key)
    prompt = f"""
    Answer the question using below context only

    context:
    {context}

    Question:
    {question}
    """

    response = openai_client.chat.completions.create(model = "gpt-4.1-mini",message=[{"role":"user","content":prompt}])
    final_answer= response.choice[0].message.content
    return final_answer


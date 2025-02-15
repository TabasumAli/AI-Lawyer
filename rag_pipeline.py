# from langchain_groq import ChatGroq
# from vector_database import faiss_db
# from langchain_core.prompts import ChatPromptTemplate
# from dotenv import load_dotenv


# # Load environment variables
# load_dotenv()

# # ✅ Step 1: Setup LLM
# llm_model = ChatGroq(model="deepseek-r1-distill-llama-70b")


# #Step2: Retrieve Docs

# def retrieve_docs(query):
#     return faiss_db.similarity_search(query)

# def get_context(documents):
#     context = "\n\n".join([doc.page_content for doc in documents])
#     return context

# #Step3: Answer Question

# custom_prompt_template = """
# Use the pieces of information provided in the context to answer user's question.
# If you dont know the answer, just say that you dont know, dont try to make up an answer. 
# Dont provide anything out of the given context
# Question: {question} 
# Context: {context} 
# Answer:
# """

# # def answer_query(documents, model, query):
# #     context = get_context(documents)
# #     prompt = ChatPromptTemplate.from_template(custom_prompt_template)
# #     chain = prompt | model
# #     return chain.invoke({"question": query, "context": context})


# def answer_query(documents, model, query):
#     context = get_context(documents)
#     prompt = ChatPromptTemplate.from_template(custom_prompt_template)
#     chain = prompt | model
#     output = chain.invoke({"question": query, "context": context})
#     # Since output is an AIMessage, use its content attribute
#     answer_text = output.content
#     return answer_text


# #question="If a government forbids the right to assemble peacefully which articles are violated and why?"
# #retrieved_docs=retrieve_docs(question)
# #print("AI Lawyer: ",answer_query(documents=retrieved_docs, model=llm_model, query=question))
from langchain_groq import ChatGroq
from vector_database import faiss_db
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

# ✅ Step 1: Load API Key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]  # Read from secrets.toml

# ✅ Step 2: Initialize LLM
llm_model = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY)

# ✅ Step 3: Retrieve Docs
def retrieve_docs(query):
    return faiss_db.similarity_search(query)

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

# ✅ Step 4: Answer Query
custom_prompt_template = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context
Question: {question} 
Context: {context} 
Answer:
"""

def answer_query(documents, model, query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model
    output = chain.invoke({"question": query, "context": context})
    return output.content  # Extract text from AIMessage

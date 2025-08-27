import sys
import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing_extensions import TypedDict

# Use current working directory for notebooks
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from ..state.state_llm import ChatMessage
from ..tools.index_search import search_index_gdpr
from ..llm.graph_llm import source_llm
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage

load_dotenv()

def chat_func(state: ChatMessage):
    llm = source_llm().get_llm_model()
    llm = llm.bind_tools([search_index_gdpr])
    system_prompt = (
        "You are a GDPR expert. Answer the question based on the context provided and your own understanding. "
        "If you don't know the answer, just say that you don't know, don't try to make up an answer."
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["messages"])
    ]
    response = llm.invoke(messages)
    return {"messages": response.content}

def chat_func2(state: ChatMessage):
    llm = source_llm().get_llm_model()
    llm = llm.bind_tools([search_index_gdpr])
    system_prompt = f"""You are a GDPR expert. Answer the question based on the context provided and your own understanding.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        User question: {state['messages']}"""
   
    response = llm.invoke(system_prompt)
    return {"messages": [AIMessage(content=response.content)]}
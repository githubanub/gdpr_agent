import sys
import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing_extensions import TypedDict

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from langgraph.graph import StateGraph, START, END
from ..state.state_llm import ChatMessage
from ..nodes.chat_nodes import chat_func,chat_func2
load_dotenv()

def graph_func():
    chat_graph=StateGraph(ChatMessage)
    chat_graph.add_node("chatnode",chat_func2)
    chat_graph.add_edge(START,"chatnode")
    chat_graph.add_edge("chatnode",END)
    chat_graph_run=chat_graph.compile()
    return chat_graph_run
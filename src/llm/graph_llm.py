import os
import sys

# Use current working directory for relative imports
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class source_llm:
    def __init__(self,
                 model_name="deepseek-r1-distill-llama-70b",
                 temperature=0.1):
        self.model_name=model_name
        self.temperature=temperature
    
    def get_llm_model(self):
        llm = ChatGroq(model=self.model_name,
                      temperature=self.temperature,)
        return llm

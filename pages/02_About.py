# pylint: disable=invalid-name
"""Collection's Page"""
import streamlit as st
import openai
from app.chroma_client import ChromaDB

chroma_db = ChromaDB(openai.api_key)

st.header("About")

# A summary of the project
st.write(
    """
    GnosisPages was developed by
    [J.P. Pérez Tejada](https://www.linkedin.com/in/juanpaulopereztejada/). December, 2023.
    
    
    Check the [GitHub repository](https://github.com/maclenn77/pdf-explainer) for more information.
    """
)

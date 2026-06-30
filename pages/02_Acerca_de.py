# pylint: disable=invalid-name
"""Collection's Page"""
import streamlit as st
import openai
from gnosis.chroma_client import ChromaDB

chroma_db = ChromaDB(openai.api_key)

st.header("About")

# A summary of the project
st.write(
    """
    Explorador de CVs fue desarrollado por
    [J.P. Pérez Tejada](https://www.linkedin.com/in/juanpaulopereztejada/). Junio, 2026.

    Maestría de Inteligencia Artifiicial Aplicada, Instituto Tecnológico de Estudios Superiores de Monterrey (ITESM).
    
    
    Revisa el [repositorio de GitHub](https://github.com/maclenn77/explorador-de-cvs) para más información.
    """
)

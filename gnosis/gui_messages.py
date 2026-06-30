"""Streamlit GUI messages."""
import streamlit as st


def header():
    """A header"""
    st.title("Explorador de CVs")
    st.subheader("Crea tu base de conocimiento")


def api_message(api_key):
    """Inform if the api key is set."""
    if api_key is None:
        return st.warning("Agrega tu clave de OpenAI API")

    return st.success("Tu clave de API está configurada")

"""Module for building the Langchain Agent"""
import os

import streamlit as st
from openai import AuthenticationError, APIConnectionError, BadRequestError
from langchain_openai import ChatOpenAI

from gnosis.agent import PDFExplainer

def build(key, client):
    """An Agent builder"""
    try:
        key = os.environ.get("OPENAI_API_KEY") or key
        llm = ChatOpenAI(
            temperature=st.session_state.temperature,
            model="gpt-4o-mini",
            api_key=key
            )
        agent = PDFExplainer(
            llm,
            client,
            extra_tools=False,
        ).agent
    except AuthenticationError:
        st.warning("Clave de OpenAI API inválida. Verifica tus credenciales.")
    except APIConnectionError:
        st.warning("No se pudo conectar a OpenAI. Verifica tu conexión de red.")
    except BadRequestError as e:
        st.warning(f"Solicitud incorrecta: {e}")
    except ValueError as e:
        st.warning(f"Error de configuración: {e}")

    return agent

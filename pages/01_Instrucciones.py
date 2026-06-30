# pylint: disable=invalid-name
"""Instrucciones de uso del sitio web"""
import streamlit as st

st.title("Cómo usar esta aplicación")
st.markdown(
    "1. **Sube un archivo PDF o PNG**: Debe ser un archivo con texto. Las páginas escaneadas sin OCR no son compatibles."
)
st.image(image="pages/images/02_Upload_PDF.png", caption="Subir un archivo PDF o PNG")
st.markdown(
    "2. **Guardar fragmentos**: El texto se extrae, divide y guarda en fragmentos en ChromaDB."
)
st.image(image="pages/images/03_Save_Chunks.png", caption="Guardar fragmentos")
st.markdown(
    "3. **Consulta tu base de conocimiento**: Usa el chatbot para hacer preguntas sobre los CVs cargados."
)
st.image(image="pages/images/04_Consult_KB.png", caption="Consulta tu base de conocimiento")
st.markdown(
    '4. **Cambia el nivel de creatividad**: También llamado "temperatura". A mayor valor, resultados más inesperados.'
)
st.image(image="pages/images/06_Creativity.png", caption="Cambiar nivel de creatividad")
st.markdown("5. **Eliminar colección**: Puedes eliminar tu colección y comenzar de nuevo.")
st.image(image="pages/images/07_Delete_Collection.png", caption="Eliminar colección")
st.write("¡Eso es todo! ¡Disfrútalo!")

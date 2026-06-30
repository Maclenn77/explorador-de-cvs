"""Sidebar component for the Streamlit app."""
import streamlit as st


def delete_collection(client, collection):
    """Delete collection button."""
    if st.button("Eliminar colección"):
        st.warning("¿Estás seguro?")
        if st.button("Sí"):
            try:
                client.delete_collection(collection.name)
            except AttributeError:
                st.error("Colección eliminada.")


def creativity_slider():
    """Slider with temperature level"""
    st.sidebar.subheader("Creatividad")
    st.sidebar.write("A mayor valor, más creativos los resultados.")
    st.sidebar.slider(
        "Temperatura",
        min_value=0.0,
        max_value=1.25,
        value=0.5,
        step=0.01,
        key="temperature",
    )


def sidebar(client, collection):
    """Sidebar component for the Streamlit app."""
    with st.sidebar:
        creativity_slider()

        delete_collection(client, collection)

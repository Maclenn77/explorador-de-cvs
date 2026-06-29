"""Main component"""
import textwrap
import tiktoken
import fitz
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
import gnosis.gui_messages as gm
from gnosis.builder import build
from gnosis.ocr import extract_text_from_image


def _save_chunks(collection, text, filename):
    """Split text into chunks and save them to the collection."""
    chunks = textwrap.wrap(text, 1250)
    encoding = tiktoken.get_encoding("cl100k_base")
    for idx, chunk in enumerate(chunks):
        num_tokens = len(encoding.encode(chunk))
        collection.add(
            documents=[chunk],
            metadatas=[{"source": filename, "num_tokens": num_tokens}],
            ids=[filename + str(idx)],
        )


def uploader(collection):
    """Component for upload files"""
    st.write(
        "Upload, extract and consult the content of PDF or PNG files for building your knowledge base!"
    )
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "png"])

    if uploaded_file is not None:
        filename = uploaded_file.name
        is_image = filename.lower().endswith(".png")

        with st.spinner("Extracting text..."):
            if is_image:
                text = extract_text_from_image(uploaded_file)
            else:
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                    text = chr(12).join([page.get_text() for page in doc])

        if not text.strip():
            st.warning("No text could be extracted from this file.")
            return

        st.subheader("Text preview")
        st.write(text[0:300] + "...")
        if st.button("Save chunks"):
            with st.spinner("Saving chunks..."):
                _save_chunks(collection, text, filename)
    else:
        st.write("Please upload a file of type: pdf or png")


def main(key, client, collection):
    """Main component"""
    gm.header()

    uploader(collection)

    st.subheader("Consult your knowledge base")

    prompt = st.chat_input()

    if prompt:
        agent = build(key, client)

        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(prompt, callbacks=[st_callback])
            st.write(response)

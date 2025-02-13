import streamlit as st
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="Text Splitter", page_icon="🚀")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def split_text_into_chunks(text, max_chars=2000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        add_len = len(word) + (1 if current_chunk else 0)
        if current_length + add_len > max_chars:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += add_len
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def generate_txt(chunks):
    return '\n\n'.join([f"--- Block {i} ---\n{chunk}" for i, chunk in enumerate(chunks, 1)])

# Streamlit UI
st.title("Document Splitter App")

uploaded_file = st.file_uploader("Upload a file", type=['txt', 'pdf', 'docx'])
max_chars = st.number_input("Maximum characters per chunk", 
                          min_value=100, 
                          max_value=10000, 
                          value=2000,
                          help="Set the maximum number of characters per text chunk")

if uploaded_file:
    # Process text extraction
    text = ""
    try:
        if uploaded_file.type == 'text/plain':
            text = uploaded_file.read().decode()
        elif uploaded_file.type == 'application/pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = extract_text_from_docx(uploaded_file)
    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.stop()

    # Split text into chunks with user-defined max size
    chunks = split_text_into_chunks(text, max_chars=max_chars)
    
    # Generate TXT output
    output = generate_txt(chunks)
    output_data = output.encode('utf-8')
    
    # Create download button
    st.download_button(
        label="Download Split Document as TXT",
        data=output_data,
        file_name="split_document.txt",
        mime="text/plain"
    )

    # Show preview
    st.subheader("Preview of First Two Chunks")
    for i, chunk in enumerate(chunks[:2], 1):
        st.write(f"**Chunk {i}** ({len(chunk)} characters)")
        st.text(chunk[:500] + "..." if len(chunk) > 500 else chunk)

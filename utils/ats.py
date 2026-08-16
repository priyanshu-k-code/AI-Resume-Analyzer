import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the embedding model only once
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    return SentenceTransformer(
        "sentence-transformers/all-mpnet-base-v2"
    )


# Function to calculate ATS similarity score
def calculate_similarity_bert(text1, text2):
    ats_model = load_embedding_model()

    embeddings1 = ats_model.encode([text1])
    embeddings2 = ats_model.encode([text2])

    # Calculate cosine similarity between resume and job description
    similarity = cosine_similarity(
        embeddings1,
        embeddings2,
    )[0][0]

    return float(max(0.0, min(1.0, similarity)))

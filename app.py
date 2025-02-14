import streamlit as st
from my_utils import query_knowledge_base, query_openrouter
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

# Set the embedding model for the application
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

#Load the vector DB
VECTOR_DB_DIR = "vector_db"
storage_context = StorageContext.from_defaults(persist_dir=VECTOR_DB_DIR)
index = load_index_from_storage(storage_context)

# Configure the Streamlit page
st.set_page_config(page_title="Solar Panel Expert Chat", layout="wide")
st.title("Solar Panel Expert Chat")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Get user input from the chat input box
user_input = st.chat_input("Ask me about solar panels...")
if user_input:
    knowledge_context = query_knowledge_base(user_input, index)
    
    # Prepare the chat context for querying the open router
    chat_context = [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in st.session_state.chat_history
    ]
    chat_context.append({"role": "system", "content": knowledge_context})
    response = query_openrouter(user_input, chat_context)
    
    # Update the chat history with the user input and assistant response
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
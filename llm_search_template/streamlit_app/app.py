import streamlit as st
import requests
import json


st.markdown("""
    <style>
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 10px;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stMarkdown {
        font-size: 20px;
        color: #333;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


st.title("💬 LLM-based RAG Search")
st.markdown("Enter your query and get an answer based on a **Retrieval-Augmented Generation (RAG)** model!")


query = st.text_input("Enter your query:", placeholder="e.g., 'What is the capital of France?'")


if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a query to proceed.")
    else:
        
        with st.spinner("Fetching the answer... Please wait"):
            
            try:
                response = requests.post(
                    'http://localhost:5001/query', 
                    json={'query': query},
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 200:
                    
                    answer = response.json().get('answer', "No answer received.")
                    st.write("### Answer: ", answer)
                else:
                    st.error(f"❌ Error: {response.status_code}")
                
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")

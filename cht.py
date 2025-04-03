import streamlit as st
import random
import datetime
import os
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain import vectorstores
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq

# Initialize LangChain LLM
@st.cache_resource()
def initialize_llm():
    return ChatGroq(
        temperature=0,
        groq_api_key="YOUR_GROQ_API_KEY",  # Replace with your API Key
        model_name="llama-3.3-70b-versatile"
    )

# Create or load Vector DB
@st.cache_resource()
def create_or_load_vector_db():
    db_path = "./chroma_db"
    if os.path.exists(db_path):
        embeddings = HuggingFaceBgeEmbeddings(model_name='all-mpnet-base-v2')
        return vectorstores.Chroma(persist_directory=db_path, embedding_function=embeddings)
    else:
        os.makedirs('./data/', exist_ok=True)
        loader = DirectoryLoader('./data/', glob='*.pdf', loader_cls=PyPDFLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)
        embeddings = HuggingFaceBgeEmbeddings(model_name='all-mpnet-base-v2')
        vector_db = vectorstores.Chroma.from_documents(texts, embeddings, persist_directory=db_path)
        vector_db.persist()
        return vector_db

# Set up QA Chain
@st.cache_resource()
def setup_qa_chain(vector_db, llm):
    retriever = vector_db.as_retriever()
    prompt_templates = """You are a supportive mental health chatbot. Answer the following question:
    {context}
    User: {question}
    Chatbot: """
    PROMPT = PromptTemplate(template=prompt_templates, input_variables=['context', 'question'])
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )

# Initialize Chatbot
llm = initialize_llm()
vector_db = create_or_load_vector_db()
qa_chain = setup_qa_chain(vector_db, llm)

def chatbot_response(user_input):
    return qa_chain.run(user_input) if user_input.strip() else "Please provide a valid input."

# Motivational & Study Prompts
def get_random_prompt(category):
    prompts = {
        "motivation": [
            "Believe in yourself! You are capable of amazing things.",
            "Success is the sum of small efforts, repeated daily.",
            "Challenges make life interesting. Overcoming them makes life meaningful.",
        ],
        "anxiety": [
            "Take a deep breath. Inhale for 4 seconds, hold for 4, and exhale for 6.",
            "Write down what’s bothering you and set it aside for later.",
            "Talk to someone you trust about what’s making you anxious.",
        ],
        "study": [
            "Use the Pomodoro technique – study for 25 mins, take a 5-min break.",
            "Summarize notes in your own words to enhance understanding.",
            "Practice active recall – test yourself instead of rereading notes.",
        ],
    }
    return random.choice(prompts[category])

# Streamlit UI
st.set_page_config(page_title="MindEase", layout="wide")
st.title("🌿 Welcome to MindEase")
st.subheader("Your personal companion for motivation, study tips, and self-care.")

# Sidebar
st.sidebar.title("MindEase Tools")
if st.sidebar.button("Need Motivation?"):
    st.sidebar.write(get_random_prompt("motivation"))
if st.sidebar.button("Feeling Anxious?"):
    st.sidebar.write(get_random_prompt("anxiety"))
if st.sidebar.button("Study Tips"):
    st.sidebar.write(get_random_prompt("study"))

# Emotion-Based Response
st.subheader("How do you feel today?")
emotion = st.selectbox("Select your emotion:", ["Happy", "Sad", "Anxious", "Motivated", "Frustrated", "Tired"])
emotion_responses = {
    "Happy": "Keep spreading joy! Happiness is contagious.",
    "Sad": "It’s okay to feel sad. Take it one step at a time.",
    "Anxious": get_random_prompt("anxiety"),
    "Motivated": "Keep up the great work! Channel your energy into goals.",
    "Frustrated": "Take a deep breath. A short break might help.",
    "Tired": "Rest is important. Give yourself time to recharge.",
}
st.write(emotion_responses[emotion])

# Study Planner
st.subheader("📖 Study Planner Generator")
num_subjects = st.number_input("Number of subjects:", min_value=1, max_value=10, step=1)
study_time = st.number_input("Total study time (in minutes):", min_value=30, step=10)
if st.button("Generate Study Plan"):
    st.write({f"Subject {i+1}": f"Study for {round(study_time / num_subjects, 2)} minutes." for i in range(int(num_subjects))})

# Chatbot
st.subheader("💬 Chat with MindEase")
user_input = st.text_input("Ask anything:")
if st.button("Send"):
    st.write(chatbot_response(user_input))

# Study Timer
st.subheader("⏳ Study Timer")
study_duration = st.number_input("Set your study duration (minutes):", min_value=10, max_value=180, step=5)
break_duration = st.selectbox("Break duration:", [5, 10, 15])
if st.button("Start Timer"):
    st.write(f"Study for {study_duration} minutes, then take a {break_duration}-minute break.")

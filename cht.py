import streamlit as st
import random
import time
import os
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

def initialize_llm():
    return ChatGroq(
        temperature=0,
        groq_api_key="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",
        model_name="llama-3.3-70b-versatile"
    )

def create_vector_db():
    embeddings = HuggingFaceBgeEmbeddings(model_name='all-mpnet-base-v2')
    return Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def setup_qa_chain(vector_db, llm):
    retriever = vector_db.as_retriever()
    prompt_templates = """You are a compassionate mental health chatbot. Respond thoughtfully:
    {context}
    user: {question}
    chatbot: """
    PROMPT = PromptTemplate(template=prompt_templates, input_variables=['context', 'question'])
    return RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": PROMPT}
    )

db_path = "./chroma_db"
if not os.path.exists(db_path):
    os.makedirs(db_path, exist_ok=True)
    vector_db = create_vector_db()
else:
    embeddings = HuggingFaceBgeEmbeddings(model_name='all-mpnet-base-v2')
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)

llm = initialize_llm()
qa_chain = setup_qa_chain(vector_db, llm)

def chatbot_response(user_input, history=[]):
    if not user_input.strip():
        return "Please provide a valid input", history
    response = qa_chain.run(user_input)
    history.append(("You", user_input))
    history.append(("🤖 MindEase", response))
    return response, history

st.set_page_config(page_title="MindEase", layout="wide")
st.markdown(
    """
    <style>
        .stApp { background-color: #f3f4f6; }
        .stSidebar { background-color: #d7e3fc; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌿 Welcome to MindEase")
st.subheader("Your personal companion for motivation, study tips, and self-care.")
st.sidebar.title("MindEase Tools")

# Prompt categories
prompts = {
    "motivation": [
        "Believe in yourself! You are capable of amazing things.",
        "Every day is a new beginning. Take a deep breath and start again.",
        "Success is the sum of small efforts, repeated daily.",
        "Keep going. Everything you need will come to you at the perfect time.",
        "Difficulties in life are intended to make us better, not bitter.",
        "You are stronger than you think. Keep pushing forward!",
        "Your potential is limitless. Never stop exploring your capabilities.",
        "The only way to achieve the impossible is to believe it is possible.",
        "Challenges are what make life interesting. Overcoming them is what makes life meaningful.",
        "You are capable, you are strong, and you can do this!"
    ],
    "anxiety": [
        "Take a deep breath. Inhale for 4 seconds, hold for 4, and exhale for 6.",
        "Close your eyes and picture your happy place. Stay there for a moment.",
        "Write down what’s bothering you and set it aside for later.",
        "Try progressive muscle relaxation – tense each muscle, then relax it.",
        "Listen to calming music or nature sounds to ease your mind.",
        "Step outside and take a short walk to clear your thoughts.",
        "Drink a warm cup of tea or water. Hydration helps relaxation.",
        "Focus on the present. What are five things you can see and hear?",
        "Talk to someone you trust about what’s making you anxious.",
        "Remind yourself: You have overcome challenges before, and you will again."
    ],
    "study": [
        "Use the Pomodoro technique – study for 25 mins, take a 5-min break.",
        "Summarize notes in your own words to enhance understanding.",
        "Teach what you learn to someone else. It helps retain information!",
        "Practice active recall – test yourself instead of rereading notes.",
        "Break large tasks into smaller chunks to avoid feeling overwhelmed.",
        "Use mnemonic devices to memorize complex concepts.",
        "Find a distraction-free study environment for better focus.",
        "Use visual aids like mind maps and diagrams to remember better.",
        "Get enough sleep! Rest is crucial for memory retention.",
        "Stay hydrated and take regular breaks to keep your mind fresh."
    ],
    "self_care": [
        "Take a 5-minute stretch break to ease your muscles.",
        "Maintain a good posture while studying to avoid back pain.",
        "Eat brain-boosting foods like nuts, fruits, and dark chocolate.",
        "Avoid excessive caffeine; try herbal tea instead.",
        "Get sunlight exposure to boost your mood and energy levels.",
        "Set realistic goals and celebrate small achievements.",
        "Listen to calming music while studying to reduce stress.",
        "Practice gratitude – write down three things you are grateful for.",
        "Take a deep breath and remind yourself it’s okay to take breaks.",
        "Limit screen time before bed to ensure better sleep quality."
    ]
}

for key, label in zip(prompts.keys(), ["Inspire Me!", "Anxiety Relief", "Study Tips", "Self-care Tips"]):
    if st.sidebar.button(label):
        st.sidebar.write(random.choice(prompts[key]))

selected_option = st.sidebar.radio("Navigation", ["Home", "Chatbot"])
if selected_option == "Home":
    st.write("Explore the tools in the sidebar or interact with our chatbot!")
    timer_input = st.number_input("Set timer (minutes):", min_value=1, max_value=120, value=25, step=1)
    if st.button("Start Timer"):
        with st.empty():
            for i in range(timer_input * 60, 0, -1):
                st.write(f"⏳ Time left: {i//60} min {i%60} sec")
                time.sleep(1)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_message = st.text_input("You:", placeholder="Ask me anything!", key="user_input")
if user_message:
    bot_response, st.session_state["chat_history"] = chatbot_response(user_message, st.session_state["chat_history"])
    for sender, message in st.session_state["chat_history"]:
        st.write(f"**{sender}:** {message}")

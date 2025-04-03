import streamlit as st
import random
import datetime

# Motivational Prompts
motivation_prompts = [
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
]

# Anxiety Relief Prompts
anxiety_relief_prompts = [
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
]

# Chatbot responses based on emotions
chatbot_responses = {
    "Happy": ["That’s amazing! Keep spreading the joy! 😊", "What made you happy today?"],
    "Sad": ["I’m here for you. It’s okay to feel this way. Do you want to talk about it?", "Remember, tough times don’t last forever."],
    "Anxious": ["Try a deep breathing exercise: Inhale for 4 seconds, hold for 4, and exhale for 6.", "Want me to guide you through a quick relaxation exercise?"],
    "Motivated": ["That’s great! What’s one goal you’re working on today?", "Stay focused and keep pushing forward! 🚀"],
    "Frustrated": ["Take a deep breath. A short break might help clear your mind.", "Do you want a quick tip to help ease your frustration?"],
    "Tired": ["Rest is just as important as work. Give yourself a moment to recharge.", "Would you like a relaxation tip?"]
}

st.set_page_config(page_title="MindEase", layout="wide")
st.title("🌿 Welcome to MindEase")
st.subheader("Your personal companion for motivation, study tips, and self-care.")

# Emotion-Based Prompt System
st.subheader("How do you feel today?")
emotion = st.selectbox("Select your emotion:", chatbot_responses.keys())
st.write(random.choice(chatbot_responses[emotion]))

# Simple Chatbot
st.subheader("💬 Chat with MindEase")
user_input = st.text_input("Type your response or ask for advice:")
if user_input:
    st.write(random.choice(chatbot_responses[emotion]))

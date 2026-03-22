import streamlit as st
import requests
import time
import speech_recognition as sr

# -------------------------------
# 🎯 Therapist Prompt
# -------------------------------
SYSTEM_PROMPT = """
You are a highly skilled, empathetic AI therapist.

- Be warm, calm, and supportive
- Validate emotions
- Ask thoughtful questions
- Avoid robotic replies
"""

# -------------------------------
# 🧠 Emotion Detection
# -------------------------------
def detect_emotion(text):
    text = text.lower()

    if "sad" in text:
        return "sad"
    elif "happy" in text:
        return "happy"
    elif "angry" in text:
        return "angry"
    elif "anxious" in text:
        return "anxious"
    else:
        return "neutral"

# -------------------------------
# 🎤 Voice Input
# -------------------------------
def listen_voice():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return ""

# -------------------------------
# 🤖 Faster Response
# -------------------------------
def get_response(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 120
                }
            }
        )
        return res.json().get("response", "")
    except:
        return "⚠️ Ollama not running"

# -------------------------------
# Prompt Builder
# -------------------------------
def build_prompt(user_input, emotion):
    return f"""
{SYSTEM_PROMPT}

User emotion: {emotion}

User: {user_input}
AI:
"""

# -------------------------------
# UI
# -------------------------------
st.title("🧠 AI Therapist Pro")
st.write("I'm here to support you 💙")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Voice button
if st.button("🎤 Speak"):
    user_input = listen_voice()
else:
    user_input = st.chat_input("How are you feeling?")

if user_input:
    emotion = detect_emotion(user_input)
    st.caption(f"Emotion: {emotion}")

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""

        with st.spinner("Thinking..."):
            prompt = build_prompt(user_input, emotion)
            reply = get_response(prompt)

        for word in reply.split():
            full += word + " "
            time.sleep(0.02)
            placeholder.markdown(full + "▌")

        placeholder.markdown(full)

    st.session_state.messages.append({"role": "assistant", "content": full})
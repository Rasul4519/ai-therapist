import streamlit as st
from app import detect_emotion, build_prompt, get_response

st.set_page_config(page_title="AI Therapist 💙", layout="centered")

st.title("💙 AI Therapist")
st.caption("Talk freely. I'm here to listen.")

# 🔹 Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🔹 User input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔹 Detect emotion
    emotion = detect_emotion(user_input)

    # 🔹 Build prompt
    prompt = build_prompt(user_input, emotion)

    # 🔹 Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_response(prompt)
            st.markdown(reply)

    # Save AI message
    st.session_state.messages.append({"role": "assistant", "content": reply})

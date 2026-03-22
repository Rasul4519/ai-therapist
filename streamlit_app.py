import streamlit as st
from app import detect_emotion, build_prompt, get_response

st.set_page_config(page_title="AI Therapist", page_icon="🧠")

st.title("🧠 AI Therapist")
st.caption("I'm here to listen and support you 💙")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # Detect emotion
    emotion = detect_emotion(user_input)
    st.caption(f"Detected emotion: {emotion}")

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.spinner("Thinking..."):
            prompt = build_prompt(st.session_state.messages)
            ai_reply = get_response(prompt)

        # Typing effect
        full_response = ""
        for word in ai_reply.split():
            full_response += word + " "
            message_placeholder.markdown(full_response)

        # Save AI response
        st.session_state.messages.append({"role": "assistant", "content": full_response})

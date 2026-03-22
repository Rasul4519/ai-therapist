import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Therapist", page_icon="💙")

st.title("💙 AI Therapist")
st.caption("Talk freely. I'm here to listen.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("How are you feeling today?")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response (FAST model)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 🔥 fast + cheap + good
            messages=[
                {
                    "role": "system",
                    "content": """You are a kind, empathetic AI therapist.
- Be supportive and understanding
- Ask gentle follow-up questions
- Keep responses short but meaningful
- Help user reflect on feelings
"""
                }
            ] + st.session_state.messages,
            temperature=0.7,
            max_tokens=200,
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "⚠️ Something went wrong. Please check your API key."

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

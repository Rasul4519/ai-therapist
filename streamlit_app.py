import streamlit as st
from openai import OpenAI

# 🔥 Fast OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Therapist 💙", layout="centered")

st.title("💙 AI Therapist")
st.caption("Talk freely. I'm here to listen.")

# 🔹 Emotion detection (fast)
def detect_emotion(text):
    text = text.lower()

    if any(w in text for w in ["sad", "depressed", "cry", "down"]):
        return "sad"
    elif any(w in text for w in ["fail", "failed", "bad", "upset"]):
        return "frustrated"
    elif any(w in text for w in ["happy", "good", "great"]):
        return "happy"
    elif any(w in text for w in ["angry", "mad"]):
        return "angry"

    return "neutral"

# 🔹 Prompt (optimized for speed + quality)
def build_prompt(user_input, emotion):
    return f"""
You are a caring AI therapist.

User emotion: {emotion}
User message: "{user_input}"

Respond briefly but warmly:
- Show empathy
- Validate feelings
- Ask 1 helpful question

Keep it natural and human-like.
"""

# 🔹 FAST response (low latency model)
def get_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ⚡ FAST + CHEAP
            messages=[
                {"role": "system", "content": "You are a kind AI therapist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {e}"

# 🔹 Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🔹 Input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    emotion = detect_emotion(user_input)
    prompt = build_prompt(user_input, emotion)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_response(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

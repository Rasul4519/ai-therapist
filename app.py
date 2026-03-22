import requests
import speech_recognition as sr

# -------------------------------
# 🎯 Advanced Therapist Prompt
# -------------------------------
SYSTEM_PROMPT = """
You are a highly skilled, empathetic AI therapist.

Your goals:
- Help users feel heard, understood, and supported
- Reflect their emotions clearly
- Ask meaningful, open-ended questions
- Encourage gentle self-reflection

Rules:
- Be warm, calm, and non-judgmental
- NEVER give harsh advice
- Avoid robotic replies
- Do NOT repeat yourself

Style:
- Natural human tone
- Short paragraphs
- Calm and thoughtful
"""

# -------------------------------
# 🧠 Emotion Detection
# -------------------------------
def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in ["sad", "depressed", "unhappy", "cry"]):
        return "sad"
    elif any(word in text for word in ["happy", "good", "great", "awesome"]):
        return "happy"
    elif any(word in text for word in ["angry", "mad", "frustrated"]):
        return "angry"
    elif any(word in text for word in ["anxious", "worried", "nervous"]):
        return "anxious"
    else:
        return "neutral"

# -------------------------------
# 🎤 Voice Input
# -------------------------------
def listen_voice():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You (voice):", text)
        return text
    except:
        print("❌ Could not understand audio")
        return ""

# -------------------------------
# 🤖 Get Response (FAST)
# -------------------------------
def get_response(prompt):
    try:
        response = requests.post(
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
        return response.json().get("response", "No response")
    except:
        return "⚠️ Make sure Ollama is running!"

# -------------------------------
# 🧱 Build Prompt
# -------------------------------
def build_prompt(user_input, emotion):
    return f"""
{SYSTEM_PROMPT}

The user is feeling: {emotion}

Respond accordingly:
- sad → comfort
- anxious → reassure
- angry → calm
- happy → encourage

User: {user_input}
AI:
"""

# -------------------------------
# 💬 Chat Loop
# -------------------------------
def chat():
    print("🧠 AI Therapist (CLI + Voice)")
    print("Type 'exit' to quit.\n")

    while True:
        mode = input("Type or Voice? (t/v): ")

        if mode == "v":
            user_input = listen_voice()
        else:
            user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Take care 💙")
            break

        emotion = detect_emotion(user_input)
        print(f"💡 Emotion: {emotion}")

        prompt = build_prompt(user_input, emotion)
        ai_reply = get_response(prompt)

        print("\nAI:", ai_reply)
        print("-" * 50)


if __name__ == "__main__":
    chat()
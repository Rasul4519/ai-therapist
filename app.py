import requests

# 🔹 Emotion Detection
def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in ["sad", "depressed", "cry", "down"]):
        return "sad"
    elif any(word in text for word in ["fail", "failed", "bad", "upset"]):
        return "frustrated"
    elif any(word in text for word in ["happy", "good", "great"]):
        return "happy"
    elif any(word in text for word in ["angry", "mad"]):
        return "angry"

    return "neutral"


# 🔹 Prompt Builder (Improved Therapy Quality)
def build_prompt(user_input, emotion):
    return f"""
You are a kind, supportive AI therapist.

User emotion: {emotion}

User says: "{user_input}"

Respond with:
- Show empathy first
- Validate feelings
- Ask a gentle follow-up question
- Give helpful advice if needed

Keep it short, natural, and human-like.
"""


# 🔹 Get Response from Ollama (FASTER)
def get_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get("response", "No response")
        else:
            return "⚠️ Error: Ollama not responding"

    except:
        return "⚠️ Make sure Ollama is running!"


# 🔹 CLI Version (Optional)
if __name__ == "__main__":
    print("🤖 AI Therapist (CLI VERSION)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        emotion = detect_emotion(user_input)
        print(f"🧠 Detected emotion: {emotion}")

        prompt = build_prompt(user_input, emotion)
        reply = get_response(prompt)

        print("AI:", reply)
        print("-" * 50)

import requests

# Therapist system prompt
SYSTEM_PROMPT = """
You are a professional, empathetic AI therapist.

Rules:
- Always be warm, calm, and supportive
- Validate the user's feelings
- Ask thoughtful follow-up questions
- Keep responses natural and human-like
- Avoid being repetitive
- Do NOT give harsh advice
- Focus on emotional support and reflection

Style:
- Talk like a real human therapist
- Use short paragraphs
- Be gentle and understanding
"""

# Emotion detection
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


# Build prompt
def build_prompt(messages):
    prompt = SYSTEM_PROMPT + "\n\n"

    for msg in messages:
        role = "User" if msg["role"] == "user" else "Therapist"
        prompt += f"{role}: {msg['content']}\n"

    prompt += "Therapist:"
    return prompt


# ⚠️ TEMP RESPONSE (since Ollama won't work on cloud)
def get_response(prompt):
    return "I'm here with you. Tell me more about what you're feeling right now 💙"

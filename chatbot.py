from google import genai

# API KEY
client = genai.Client(api_key="AIzaSyB5mJGdbvsTGyWl8N1m9V9qCuutmHrryH0")

MODEL_NAME = "gemini-2.5-flash"

def ask_chatbot(user_message):

    prompt = f"""
    You are a professional fitness trainer and diet expert.

    Answer the user's question about:
    - gym workout
    - fat loss
    - muscle gain
    - vegetarian diet
    - fitness tips

    User question: {user_message}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text
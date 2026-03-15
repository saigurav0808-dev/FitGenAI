import google.generativeai as genai

# API KEY
genai.configure(api_key="AIzaSyAOaYBI9kK6-KWHb5ytAx8V6mOqr-R2570")

model = genai.GenerativeModel("gemini-2.5-flash")

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

    response = model.generate_content(prompt)

    return response.text
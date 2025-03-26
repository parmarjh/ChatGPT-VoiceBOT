import openai
import speech_recognition as sr
import pyttsx3
from flask import Flask, request, jsonify

app = Flask(__name__)

gpt_api_key = "YOUR_OPENAI_API_KEY"

engine = pyttsx3.init()

def chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Speech Recognition service error"

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    user_input = data.get("question", "")
    if not user_input:
        return jsonify({"error": "No question provided"}), 400
    
    response_text = chatgpt_response(user_input)
    text_to_speech(response_text)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)

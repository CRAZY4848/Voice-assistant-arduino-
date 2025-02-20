 import serial
import speech_recognition as sr
from difflib import get_close_matches
import ollama

# Load FAQ data
faq_data = {}
with open("college_faq.txt", "r", encoding="utf-8") as f:
    for line in f:
        question, answer = line.strip().split(":", 1)
        faq_data[question.lower()] = answer.strip()

# Function to find the best FAQ match
def get_faq_answer(question):
    matches = get_close_matches(question.lower(), faq_data.keys(), n=1, cutoff=0.7)
    if matches:
        return faq_data[matches[0]]
    return None

# Function to get AI-generated response from Llama 3.2
def get_llama_response(question):
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": question}])
    return response["message"]["content"][:32]  # Limit to 32 characters

# Initialize microphone and serial communication
recognizer = sr.Recognizer()
mic = sr.Microphone()
arduino = serial.Serial('COM3', 9600)  # Change to the correct port (e.g., /dev/ttyUSB0 for Linux)

print("Assistant is running...")

while True:
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio)
        print("User asked:", question)

        # First check the FAQ
        answer = get_faq_answer(question)
        if not answer:
            answer = get_llama_response(question)  # If not in FAQ, ask Llama 3.2

        # Send answer to Arduino
        print("Answer:", answer)
        arduino.write((answer + "\n").encode())

    except Exception as e:
        print("Error:", str(e))

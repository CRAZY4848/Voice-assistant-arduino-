import serial
import speech_recognition as sr
from difflib import get_close_matches
import ollama

# Load FAQ data properly
faq_data = {}
with open("college_faq.txt", "r", encoding="utf-8") as f:
    question = None
    for line in f:
        line = line.strip()
        if line.startswith("Q: "):  
            question = line.replace("Q: ", "").strip()  # Remove "Q: "
        elif line.startswith("A: ") and question:
            answer = line.replace("A: ", "").strip()  # Remove "A: "
            faq_data[question.lower()] = answer  # Store in dictionary

# Function to find the best FAQ match
def get_faq_answer(question):
    question = question.lower().strip()  # Normalize input
    matches = get_close_matches(question, faq_data.keys(), n=1, cutoff=0.4)  # Looser cutoff

    print("\n📝 User Question:", question)
    print("🔍 Closest Match Found:", matches)

    if matches:
        return faq_data[matches[0]]

    # 🔥 **New: Smarter Keyword Matching**
    best_match = None
    highest_match_score = 0

    for faq_question in faq_data.keys():
        words_in_question = set(question.split())
        words_in_faq = set(faq_question.split())

        common_words = words_in_question & words_in_faq  # Find common words

        match_score = len(common_words) / max(len(words_in_question), len(words_in_faq))  # Match percentage

        if match_score > 0.4 and len(common_words) > 1:  # Ensure at least 2 words match
            if match_score > highest_match_score:
                highest_match_score = match_score
                best_match = faq_question

    if best_match:
        print("✅ Best Match Found:", best_match)
        return faq_data[best_match]

    return None  # No match found

# Function to get AI-generated response from Llama 3.2
def get_llama_response(question):
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": question}])
    return response["message"]["content"][:32]  # Limit to 32 characters for LCD

# Initialize microphone and serial communication
recognizer = sr.Recognizer()
mic = sr.Microphone()
arduino = serial.Serial('COM12', 9600)  # Change to the correct port (e.g., /dev/ttyUSB0 for Linux)

print("Assistant is running...")

while True:
    with mic as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio)
        print("📝 User asked:", question)

        # First check the FAQ
        answer = get_faq_answer(question)
        if not answer:
            print("❌ Not found in FAQ, sending to Llama...")
            answer = get_llama_response(question)  # If not in FAQ, ask Llama 3.2

        # Send answer to Arduino
        print("💡 Answer:", answer)
        arduino.write((answer + "\n").encode())

    except Exception as e:
        print("⚠️ Error:", str(e))

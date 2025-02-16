import speech_recognition as sr
import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=1)  # Change COM port if needed
time.sleep(2)  # Wait for Arduino to initialize

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except:
        return ""

while True:
    command = listen()

    if "turn on light" in command:
        arduino.write(b"turn on light\n")
    elif "turn off light" in command:
        arduino.write(b"turn off light\n")
    elif "exit" in command:
        break

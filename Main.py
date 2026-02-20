from Backend.Chatbot import chatbot
from Backend.SpeechToText import listen
from Backend.TextToSpeech import speak

print("🎤 Ravi Voice Assistant Started (Say 'exit' to stop)")

while True:
    user_input = listen()

    if "exit" in user_input.lower():
        speak("Goodbye Ravi")
        break

    reply = chatbot(user_input)

    print("AI:", reply)
    speak(reply)

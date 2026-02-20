import speech_recognition as sr

def listen(language="auto"):
    """
    Listen from mic and convert speech to text.
    language: Google SpeechRecognition language code (default: "auto")
        Examples:
        - "hi-IN" → Hindi
        - "en-US" → English
        - "en-IN" → Indian English
        - "auto" → fallback to Hindi+English dynamically
    """
    recognizer = sr.Recognizer()

    try:
        mic = sr.Microphone(device_index=1)  # Change index if needed

        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)

        print("Recognizing...")

        # Auto language detection: fallback to hi-IN + en-US
        if language == "auto":
            try:
                text = recognizer.recognize_google(audio, language="hi-IN")
                return text
            except sr.UnknownValueError:
                # Try English if Hindi fails
                text = recognizer.recognize_google(audio, language="en-US")
                return text
        else:
            text = recognizer.recognize_google(audio, language=language)
            return text

    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return "Sorry, I didn't understand."
    except Exception as e:
        return f"Mic Error: {e}"

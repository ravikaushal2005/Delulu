import asyncio
import edge_tts
import uuid
import os
import threading
from playsound import playsound
from queue import Queue

VOICE = "hi-IN-SwaraNeural"  # 🔥 voice female

audio_queue = Queue()
is_speaking = False


# ---------------- GENERATE AUDIO ---------------- #
async def generate_audio(text, filename):
    # 🔥 20% faster
    communicate = edge_tts.Communicate(text, VOICE, rate="+17%")
    await communicate.save(filename)


# ---------------- AUDIO WORKER ---------------- #
def audio_worker():
    global is_speaking

    while True:
        text = audio_queue.get()
        filename = f"temp_{uuid.uuid4()}.mp3"

        try:
            is_speaking = True
            asyncio.run(generate_audio(text, filename))
            playsound(filename)  # Waits until finished
        except Exception as e:
            print("TTS Error:", e)
        finally:
            is_speaking = False
            if os.path.exists(filename):
                os.remove(filename)  # Cleanup temp file

        audio_queue.task_done()


# 🔥 Start only ONE worker thread
threading.Thread(target=audio_worker, daemon=True).start()


# ---------------- PUBLIC FUNCTIONS ---------------- #
def speak(text):
    if text and text.strip():
        audio_queue.put(text)


def wait_until_done():
    audio_queue.join()
def speak(text, auto_speak=True):
    # auto_speak=True tabhi speak kare
    if text and text.strip() and auto_speak:
        audio_queue.put(text)

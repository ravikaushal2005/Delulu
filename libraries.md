from dotenv import load_dotenv
import os
from groq import Groq

import speech_recognition as sr
import asyncio
import edge_tts
import uuid
import os
import threading
from playsound import playsound
from queue import Queue
import sys
import os
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import scrolledtext, messagebox
import customtkinter as ctk

from Backend.Chatbot import chatbot
from Backend.SpeechToText import listen
from Backend.TextToSpeech import speak, wait_until_done
from Backend.Automatation import Automation
from Backend.Chatbot import chatbot
from Backend.SpeechToText import listen
from Backend.TextToSpeech import speak

pip install python-dotenv groq SpeechRecognition edge-tts playsound==1.2.2 PyAudio customtkinter pyinstaller
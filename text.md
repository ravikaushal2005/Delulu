import sys
import os
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import scrolledtext

from Backend.Chatbot import chatbot
from Backend.SpeechToText import listen
from Backend.TextToSpeech import speak, wait_until_done


class RaviAIApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Ravi AI Assistant")
        self.root.geometry("650x750")
        self.root.configure(bg="#121212")

        self.is_listening = False

        self.create_widgets()

    # ---------------- UI ---------------- #

    def create_widgets(self):

        header = tk.Label(
            self.root,
            text="🤖 Ravi AI Assistant",
            bg="#1f1f1f",
            fg="white",
            font=("Arial", 18, "bold"),
            pady=10
        )
        header.pack(fill=tk.X)

        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="white",
            font=("Consolas", 12),
            state="disabled"
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(self.root, bg="#121212")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(
            input_frame,
            font=("Arial", 14),
            bg="#2a2a2a",
            fg="white",
            insertbackground="white"
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", lambda event: self.send_message())

        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg="#3a7ff6",
            fg="white",
            font=("Arial", 12, "bold"),
            width=8
        )
        send_button.pack(side=tk.RIGHT)

        self.mic_button = tk.Button(
            input_frame,
            text="🎤",
            command=self.voice_input,
            bg="#00aa88",
            fg="white",
            font=("Arial", 12, "bold"),
            width=4
        )
        self.mic_button.pack(side=tk.RIGHT, padx=5)

        self.status = tk.Label(
            self.root,
            text="Status: Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#1f1f1f",
            fg="white"
        )
        self.status.pack(fill=tk.X)

    # ---------------- SEND MESSAGE ---------------- #

    def send_message(self):

        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.display_message("You", user_input, "#00ffcc")
        self.entry.delete(0, tk.END)
        self.update_status("Thinking...")

        def process():
            try:
                reply = chatbot(user_input)

                self.root.after(0, lambda: self.display_message("AI", reply, "#ffcc00"))
                self.root.after(0, lambda: self.update_status("Ready"))

                speak(reply)   # 🔥 NO extra thread

            except Exception as e:
                self.root.after(0, lambda: self.display_message("System", f"Error: {e}", "red"))
                self.root.after(0, lambda: self.update_status("Error"))

        threading.Thread(target=process, daemon=True).start()

    # ---------------- VOICE INPUT ---------------- #

    def voice_input(self):

        if self.is_listening:
            return

        wait_until_done()  # 🔥 Ensure AI finished speaking

        self.is_listening = True
        self.mic_button.config(state="disabled")
        self.update_status("Listening...")

        def process():
            try:
                text = listen()

                if text:
                    self.root.after(0, lambda: self.entry.delete(0, tk.END))
                    self.root.after(0, lambda: self.entry.insert(0, text))
                    self.root.after(0, self.send_message)

            except Exception as e:
                self.root.after(0, lambda: self.display_message("System", f"Mic Error: {e}", "red"))

            finally:
                self.is_listening = False
                self.root.after(0, lambda: self.mic_button.config(state="normal"))
                self.root.after(0, lambda: self.update_status("Ready"))

        threading.Thread(target=process, daemon=True).start()

    # ---------------- HELPERS ---------------- #

    def display_message(self, sender, message, color):

        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, f"{sender}: ", ("tag",))
        self.chat_area.insert(tk.END, message + "\n\n")
        self.chat_area.tag_config("tag", foreground=color, font=("Arial", 12, "bold"))
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

    def update_status(self, text):
        self.status.config(text=f"Status: {text}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RaviAIApp(root)
    root.mainloop()

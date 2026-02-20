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

auto = Automation()

# 🔥 CustomTkinter global settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RaviAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Delulu AI")
        self.root.geometry("700x800")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.is_listening = False
        self.create_widgets()

    # ---------------- UI ---------------- #

    def create_widgets(self):

        # HEADER FRAME
        header_frame = tk.Frame(self.root, bg="#111827", height=60)
        header_frame.pack(fill=tk.X)

        # 🔥 Center Title
        title = tk.Label(
            header_frame,
            text="🤖 Delulu",
            bg="#111827",
            fg="#38bdf8",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=15)  # Center automatically

        # About button (top-right using place)
        about_btn = tk.Button(
            header_frame,
            text="ℹ",
            command=self.show_about,
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            bd=0,
            width=3,
            cursor="hand2"
        )
        about_btn.place(relx=0.95, rely=0.5, anchor="center")

        # CHAT AREA
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            bg="#1e293b",
            fg="white",
            font=("Consolas", 12),
            state="disabled",
            bd=0
        )
        self.chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        # INPUT FRAME
        input_frame = tk.Frame(self.root, bg="#111827")
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        # 🔥 Rounded Entry
        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message...",
            corner_radius=10,
            font=("Segoe UI", 18),
            height=40,
            bg_color="#0f1e38"
           
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.send_message())

        # 🔥 Rounded Send Button
        send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_message,
            corner_radius=10,
            width=80,
            height=40
        )
        send_button.pack(side=tk.RIGHT)

        # 🔥 Rounded Mic Button
        self.mic_button = ctk.CTkButton(
            input_frame,
            text="🎤",
            command=self.voice_input,
            corner_radius=20,
            width=50,
            height=40,
            fg_color="#10b981",
            hover_color="#059988"
        )
        self.mic_button.pack(side=tk.RIGHT, padx=8)

        # STATUS BAR
        self.status = tk.Label(
            self.root,
            text="Status: Ready",
            bg="#111827",
            fg="#94a3b8",
            font=("Segoe UI", 10),
            anchor=tk.W
        )
        self.status.pack(fill=tk.X, pady=(5, 0))

    # ---------------- ABOUT ---------------- #

    def show_about(self):
        messagebox.showinfo(
            "About Delulu",
            "Delulu AI Assistant\n\n"
            "Developer: Ravi Kaushal\n"
            "Version: 1.0\n\n"
            "Features:\n"
            "- AI Chatbot\n"
            "- Voice Commands\n"
            "- Automation System\n\n"
            "Made with ❤️ using Python"
        )

    # ---------------- SEND MESSAGE ---------------- #

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.display_message("You", user_input, "#22d3ee")
        self.entry.delete(0, tk.END)
        self.update_status("Thinking...")

        def process():
            try:
                reply = chatbot(user_input)

                self.root.after(0, lambda: self.display_message("DELULU", reply, "#facc15"))
                self.root.after(0, lambda: self.update_status("Ready"))

                speak(reply)

            except Exception as e:
                self.root.after(0, lambda: self.display_message("System", f"Error: {e}", "red"))
                self.root.after(0, lambda: self.update_status("Error"))

        threading.Thread(target=process, daemon=True).start()

    # ---------------- VOICE INPUT ---------------- #

    def voice_input(self):
        if self.is_listening:
            return

        wait_until_done()

        self.is_listening = True
        self.mic_button.configure(state="disabled")
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
                self.root.after(0, lambda: self.mic_button.configure(state="normal"))
                self.root.after(0, lambda: self.update_status("Ready"))

        threading.Thread(target=process, daemon=True).start()

    # ---------------- HELPERS ---------------- #

    def display_message(self, sender, message, color):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, f"{sender}: ", ("tag",))
        self.chat_area.insert(tk.END, message + "\n\n")
        self.chat_area.tag_config("tag", foreground=color, font=("Segoe UI", 11, "bold"))
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

    def update_status(self, text):
        self.status.config(text=f"Status: {text}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RaviAIApp(root)
    root.mainloop()
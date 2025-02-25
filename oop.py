from gtts import gTTS, lang
import os
import platform
from tkinter import *
from tkinter import messagebox
import speech_recognition as sr

def text_to_speech():
    text = text_entry.get("1.0", "end-1c")
    language = accent_entry.get()
    if (len(text) <= 1) | (len(language) <= 0):
        messagebox.showerror("Error", "Please enter text and language")
        return
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save("speech.mp3")
    if platform.system() == "Windows":
        os.system("start speech.mp3")
    else:
        os.system("mpg321 speech.mp3")
    
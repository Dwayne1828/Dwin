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

def list_languages():
    languages = lang.tts_langs()
    language_list = "\n".join([f"{key}: {value}" for key, value in languages.items()])
    messagebox.showinfo(message= language_list)

def speech_to_text():
    recognizer = sr.Recognizer()
    try: 
        duration = int(duration_entry.get())
    except:
        messagebox.showerror("Error", "Please enter a valid duration")
        return

    with sr.Microphone() as source:
        messagebox.showinfo(message = "Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=duration)
        messagebox.showinfo(message= "Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            messagebox.showinfo(message= "You said:\n " + text) 
        except:
            messagebox.showerror(message= "Error, could not recognize your voice")

from gtts import gTTS, lang
import os
import platform
from tkinter import *
from tkinter import messagebox
import speech_recognition as sr
import threading

stop_listening_event = threading.Event()

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
    messagebox.showinfo(message=language_list)

def speech_to_text():
    recognizer = sr.Recognizer()

    def listening():
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while not stop_listening_event.is_set():
                try:
                    audio = recognizer.listen(source, timeout=30)
                    text = recognizer.recognize_google(audio)
                    messagebox.showinfo(message="You said:\n " + text)
                    break
                except sr.UnknownValueError:
                    messagebox.showerror(message="Error, could not recognize your voice")
                    break
                except sr.WaitTimeoutError:
                    messagebox.showerror(message="Error, time out")
                    break

    stop_listening_event.clear()
    threading.Thread(target=listening).start()
    show_listening_message()

def show_listening_message():
    messagebox.showinfo(message="Listening... Please speak and Click OK to stop listening")
    stop_listening_event.set()

def clear_text():
    text_entry.delete("1.0", END)

window = Tk()
window.geometry("600x400")
window.title("Text to Speech and Speech to Text")
title_label = Label(window, text="Text to Speech and Speech to Text").pack()

text_label = Label(window, text="Enter text:").place(x=20, y=30)
text_entry = Text(window, height=5, width=50)
text_entry.place(x=110, y=20)

accent_label = Label(window, text="Enter accent:").place(x=20, y=160)
accent_entry = Entry(window, width=26)
accent_entry.place(x=110, y=160)

button1 = Button(window, text="Text to Speech", command=text_to_speech).place(x=110, y=200)
button2 = Button(window, text="Language List", command=list_languages).place(x=200, y=200)
button3 = Button(window, text="Speech to Text", command=speech_to_text).place(x=285, y=200)
button4 = Button(window, text="Clear Text", command=clear_text).place(x=110, y=120)

window.mainloop()
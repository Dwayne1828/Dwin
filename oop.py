# Description: This program is a simple text to speech and speech to text program using the Google Text-to-Speech API and Speech Recognition API. 
# Import the necessary modules
from gtts import gTTS, lang
import os
import platform
from tkinter import *
from tkinter import messagebox
import speech_recognition as sr
import threading

 # Event to stop listening for stt
stop_listening_event = threading.Event()            


# Function to convert text to speech
def text_to_speech():                                
    text = text_entry.get("1.0", "end-1c")                              # Get the text and accent from the entries
    language = accent_entry.get()                    
    if (len(text) <= 1) | (len(language) <= 0):                         # Check if the text and accent are empty return an error message
        messagebox.showerror("Error", "Please enter text and language")
        return
    speech = gTTS(text=text, lang=language, slow=False)                 # Convert the text to speech using gTTS module
    speech.save("speech.mp3")
    if platform.system() == "Windows":                                  # Play the speech using the default media player based on the OS
        os.system("start speech.mp3")
    else:
        os.system("mpg321 speech.mp3")


# Function to clear the text entry when using text to speech
def clear_text():                                    
    text_entry.delete("1.0", END)


# Function to list the available languages and their codes supported by the API
def list_languages():                                
    languages = lang.tts_langs()
    language_list = "\n".join([f"{key}: {value}" for key, value in languages.items()])
    messagebox.showinfo(message=language_list)


# A function to convert speech to text using the Speech Recognition module
def speech_to_text():                                
    recognizer = sr.Recognizer()                     

    def listening():                                
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while not stop_listening_event.is_set(): 
                try:
                    audio = recognizer.listen(source, timeout=30)                              # A function to listen for the audio input
                    text = recognizer.recognize_google(audio)                                  # recognize the speech using the Google API
                    messagebox.showinfo(message="You said:\n " + text)                         # Show the recognized text in a message box
                    break                                                                      # Then handle the exceptions and show the error message
                except sr.UnknownValueError:                                                   
                    messagebox.showerror(message="Error, could not recognize your voice")
                    break
                except sr.WaitTimeoutError:
                    messagebox.showerror(message="Error, time out")
                    break

    stop_listening_event.clear()                     # Clear the event to start listening for the audio and use a thread to run the listening function simultaenously
    threading.Thread(target=listening).start()       # Start the thread for function and message box while listening
    show_listening_message()


# Function to show the message box while listening until the user clicks OK and the event is set
def show_listening_message():                        
    messagebox.showinfo(message="Listening... Please speak and Click OK to stop listening")
    stop_listening_event.set()


# Create a GUI window using tkinter to interact with the user and call the functions
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

window.mainloop() # Run the GUI window
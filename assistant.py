import tkinter as tk
from tkinter import messagebox
import os
import pyttsx3
import pywhatkit as kit
import datetime
import random
import webbrowser
import ctypes
import time
import speech_recognition as sr  # For voice input
import requests  # For fetching weather information

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_notepad():
    speak("Opening Notepad")
    os.system("notepad")

def open_word():
    speak("Opening Microsoft Word")
    os.system("start winword")

def control_volume(action):
    """
    Controls the system volume based on the given action: increase, decrease, or mute.
    """
    VK_VOLUME_UP = 0xAF   # Virtual key code for volume up
    VK_VOLUME_DOWN = 0xAE # Virtual key code for volume down
    VK_VOLUME_MUTE = 0xAD # Virtual key code for mute

    if action == "increase":
        speak("Increasing volume")
        for _ in range(10):  # Adjust the range for desired volume increment
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)  # Press key
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)  # Release key
            time.sleep(0.05)  # Add a small delay for consistent behavior

    elif action == "decrease":
        speak("Decreasing volume")
        for _ in range(10):  # Adjust the range for desired volume decrement
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)  # Press key
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)  # Release key
            time.sleep(0.05)  # Add a small delay for consistent behavior

    elif action == "mute":
        speak("Muting volume")
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)  # Press key
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)  # Release key

def open_email_window(preference):
    if preference == "gmail":
        speak("Opening Gmail.")
        try:
            webbrowser.open("https://mail.google.com/")
            update_output("Assistant: Opened Gmail.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Gmail: {str(e)}")
    elif preference == "thunderbird":
        speak("Opening Thunderbird.")
        try:
            os.system("start thunderbird")
            update_output("Assistant: Opened Thunderbird.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Thunderbird: {str(e)}")
    else:
        speak("Invalid choice. Please choose Gmail or Thunderbird.")
        update_output("Assistant: Invalid choice. Please choose Gmail or Thunderbird.")

def ask_email_preference():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Do you want to send email using Gmail or Thunderbird?")
        update_output("Assistant: Listening for email preference...")
        try:
            audio = r.listen(source, timeout=5)
            preference = r.recognize_google(audio).lower()
            update_output(f"You said: {preference}")
            if "gmail" in preference:
                return "gmail"
            elif "thunderbird" in preference:
                return "thunderbird"
            else:
                speak("I didn't understand your preference. Defaulting to Gmail.")
                return "gmail"
        except sr.UnknownValueError:
            speak("Sorry, I did not catch that. Defaulting to Gmail.")
            return "gmail"
        except Exception as e:
            speak("Error occurred. Defaulting to Gmail.")
            return "gmail"

def tell_joke():
    jokes = [
        "Why did the programmer quit his job? Because he didn't get arrays.",
        "Why do Java developers wear glasses? Because they can't C#.",
        "Why was the computer cold? It left its Windows open!"
    ]
    joke = random.choice(jokes)
    speak(joke)
    return joke

def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")
    return f"The current time is {current_time}"

def play_music(song_name):
    """
    Plays music on YouTube using pywhatkit's playonyt method.
    It searches for the song and plays it directly.
    """
    try:
        speak(f"Searching and playing {song_name} on YouTube")
        kit.playonyt(song_name)
        update_output(f"Assistant: Playing {song_name} directly on YouTube.")
    except Exception as e:
        speak(f"Sorry, I could not play {song_name}. Error: {e}")
        update_output(f"Assistant: Sorry, I could not play {song_name}. Error: {str(e)}")


def handle_query(query):
    query = query.lower()

    if "open notepad" in query:
        open_notepad()
    elif "open word" in query:
        open_word()
    elif "increase volume" in query:
        control_volume("increase")
    elif "decrease volume" in query:
        control_volume("decrease")
    elif "mute volume" in query:
        control_volume("mute")
    elif "send email" in query:
        update_output("Assistant: Asking for email preference...")
        preference = ask_email_preference()
        open_email_window(preference)
    elif "tell me a joke" in query:
        joke = tell_joke()
        update_output(f"Assistant: {joke}")
    elif "current time" in query:
        time_info = tell_time()
        update_output(f"Assistant: {time_info}")
    elif "play music" in query:
        song_name = query.replace("play music", "").strip()
        if song_name:
            play_music(song_name)
        else:
            speak("Please specify a song name after 'play music'.")
            update_output("Assistant: Please specify a song name after 'play music'.")
    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    
    else:
        speak("Sorry, I am unable to process your request.")
        update_output("Assistant: Sorry, I am unable to process your request.")

def take_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        update_output("Assistant: Listening...")
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio).lower()
            update_output(f"You (Voice): {query}")
            handle_query(query)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please say it again.")
            update_output("Assistant: Sorry, I didn't catch that. Please say it again.")
        except Exception as e:
            speak("Error occurred while listening.")
            update_output(f"Assistant: Error: {str(e)}")

def update_output(text):
    output_text.config(state="normal")
    output_text.insert(tk.END, text + "\n")
    output_text.config(state="disabled")
    output_text.see(tk.END)

def on_ask():
    query = user_input.get()
    update_output(f"You: {query}")
    handle_query(query)
    user_input.delete(0, tk.END)

def on_delete():
    output_text.config(state="normal")
    output_text.delete(1.0, tk.END)
    output_text.config(state="disabled")

root = tk.Tk()
root.title("Voice Assistant")

output_text = tk.Text(root, wrap=tk.WORD, height=20, width=50, state="disabled")
output_text.pack(padx=10, pady=10)

user_input = tk.Entry(root, width=40)
user_input.pack(padx=10, pady=10)

ask_button = tk.Button(root, text="Ask", command=on_ask)
ask_button.pack(padx=10, pady=10)

delete_button = tk.Button(root, text="Clear", command=on_delete)
delete_button.pack(padx=10, pady=10)

send_button = tk.Button(root, text="Send Voice", command=take_voice_input)
send_button.pack(padx=10, pady=10)

root.mainloop()

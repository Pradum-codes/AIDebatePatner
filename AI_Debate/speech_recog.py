import speech_recognition as sr
import threading
import tkinter as tk

def recognize_speech(chatbox, user_input, send_message):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "\n🎤 Listening... Speak now.\n", "ai")
        chatbox.config(state=tk.DISABLED)
        chatbox.update()
        
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, f"\n🎙️ You (Voice): {text}\n", "user")
            chatbox.config(state=tk.DISABLED)
            chatbox.update()
            threading.Thread(target=send_message, args=(text,)).start()
        except sr.WaitTimeoutError:
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, "\n⚠️ Timeout! No speech detected.\n", "ai")
            chatbox.config(state=tk.DISABLED)
        except sr.UnknownValueError:
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, "\n⚠️ Could not understand speech. Try again.\n", "ai")
            chatbox.config(state=tk.DISABLED)
        except sr.RequestError:
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, "\n⚠️ Speech recognition service unavailable.\n", "ai")
            chatbox.config(state=tk.DISABLED)

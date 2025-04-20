import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import threading
import os
import logging
logging.basicConfig(level=logging.INFO)

os.environ["GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"] = ""

# Set up Gemini API Key
genai.configure(api_key="AIzaSyBhmtN74htSaKlDUVQ_LBXW29V4vTIWAKI")

# Initialize Speech Engine
engine = pyttsx3.init()


def speak_text(text):
    def run():
        local_engine = pyttsx3.init()  # Initialize engine inside thread
        local_engine.say(text)
        local_engine.runAndWait()
        local_engine.stop()  # Stop properly

    threading.Thread(target=run, daemon=True).start()

# Global Variables
debate_history = []  # Stores conversation history
context = []  # Context awareness (last 5 exchanges)
debate_mode = "Casual Debate"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "\n🎤 Listening... Speak now.\n", "ai")
        chatbox.config(state=tk.DISABLED)
        chatbox.update()
        
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Extended duration
        
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeouts
            text = recognizer.recognize_google(audio)
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, f"\n🎙️ You (Voice): {text}\n", "user")
            chatbox.config(state=tk.DISABLED)
            chatbox.update()
            
            # Directly process voice input instead of calling send_message
            timestamp = datetime.now().strftime("%H:%M:%S")
            response = debate_with_ai(text)
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, f"\n🤖 AI [{timestamp}]: {response}\n", "ai")
            chatbox.config(state=tk.DISABLED)
            debate_history.append(f"You (Voice) [{timestamp}]: {text}\nAI [{timestamp}]: {response}\n")
            speak_text(response)
            
        except sr.WaitTimeoutError:
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, "\n⚠️ Timeout! No speech detected.\n", "ai")
            chatbox.config(state=tk.DISABLED)
        except sr.UnknownValueError:
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, "\n⚠️ Could not understand speech. Try again.\n", "ai")
            chatbox.config(state=tk.DISABLED)
        except sr.RequestError as e:
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, f"\n⚠️ Speech recognition error: {str(e)}\n", "ai")
            chatbox.config(state=tk.DISABLED)
            print(f"Speech recognition error: {str(e)}")  # Log to console

def debate_with_ai(user_input):
    global context
    context.append(f"User: {user_input}")
    if len(context) > 5:
        context.pop(0)
    
    prompt = f"You are an AI debate partner. We are having a '{debate_mode}' debate.\n\n" + "\n".join(context) + "\nAI:"
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=200,
                temperature=0.7
            )
        )
        ai_response = response.text if response and hasattr(response, 'text') else "I'm not sure how to respond."
    except Exception as e:
        ai_response = f"Error communicating with AI: {str(e)}"
        print(f"Gemini API error: {str(e)}")  # Log to console
    
    context.append(f"AI: {ai_response}")
    debate_history.append(f"User: {user_input}\nAI: {ai_response}\n")
    return ai_response

def start_debate():
    global debate_mode
    debate_mode = mode_var.get()
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n🤖 AI: Let's have a '{debate_mode}' debate. What’s your argument?\n", "ai")
    chatbox.config(state=tk.DISABLED)

def send_message():
    user_text = user_input.get().strip()
    if not user_text:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")

    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n🧑‍💼 You [{timestamp}]: {user_text}\n", "user")
    chatbox.config(state=tk.DISABLED)
    chatbox.update()

    try:
        response = debate_with_ai(user_text)
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, f"\n🤖 AI [{timestamp}]: {response}\n", "ai")
        chatbox.config(state=tk.DISABLED)
        debate_history.append(f"You [{timestamp}]: {user_text}\nAI [{timestamp}]: {response}\n")
        speak_text(response)
    except Exception as e:
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, f"\n⚠️ Error processing response: {str(e)}\n", "ai")
        chatbox.config(state=tk.DISABLED)
        print(f"Error in send_message: {str(e)}")  # Log to console

    user_input.delete(0, tk.END)



def save_history():
    filename = f"Debate_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(debate_history)
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n📜 History saved as '{filename}'\n", "ai")
    chatbox.config(state=tk.DISABLED)

def summarize_debate():
    if not debate_history:
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "\n⚠️ No debate history to summarize.\n", "ai")
        chatbox.config(state=tk.DISABLED)
        return
    
    summary_prompt = "Summarize the following debate:\n\n" + "".join(debate_history)
    model = genai.GenerativeModel("gemini-1.5-flash")
    summary_response = model.generate_content(
        summary_prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=200,
            temperature=0.5
        )
    )
    summary = summary_response.text if summary_response else "Couldn't generate a summary."
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n📢 Summary: {summary}\n", "ai")
    chatbox.config(state=tk.DISABLED)

# --- Root Setup ---
root = tk.Tk()
root.title("AI Debate Partner")
root.geometry("620x750")
root.configure(bg="#f4f4f4")

# --- Top Frame: Mode Selection ---
mode_frame = tk.Frame(root, bg="#ffffff", bd=1, relief=tk.RIDGE)
mode_frame.pack(padx=15, pady=15, fill=tk.X)

tk.Label(mode_frame, text="Select Debate Mode:", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=5)
mode_var = tk.StringVar(value="Casual Debate")
modes = ["Formal Debate", "Casual Debate", "Devil’s Advocate"]
mode_dropdown = ttk.Combobox(mode_frame, textvariable=mode_var, values=modes, state="readonly", font=("Arial", 10))
mode_dropdown.pack(pady=5)
tk.Button(mode_frame, text="Start Debate", font=("Arial", 10, "bold"), command=start_debate).pack(pady=5)

# --- Middle Frame: Chatbox ---
chat_frame = tk.Frame(root, bg="#ffffff", bd=1, relief=tk.RIDGE)
chat_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

chatbox = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=70, height=20, font=("Arial", 11))
chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chatbox.config(state=tk.DISABLED)
chatbox.tag_configure("user", foreground="blue", font=("Arial", 11, "bold"))
chatbox.tag_configure("ai", foreground="green", font=("Arial", 11, "bold"))

# --- Input Frame ---
input_frame = tk.Frame(root, bg="#ffffff", bd=1, relief=tk.RIDGE)
input_frame.pack(padx=15, pady=10, fill=tk.X)

user_input = tk.Entry(input_frame, width=60, font=("Arial", 11))
user_input.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill=tk.X)

send_button = tk.Button(input_frame, text="Send", font=("Arial", 10, "bold"), command=send_message)
send_button.pack(padx=5, side=tk.LEFT)

# --- Button Panel ---
control_frame = tk.Frame(root, bg="#f4f4f4")
control_frame.pack(padx=15, pady=5)

voice_button = tk.Button(control_frame, text="🎤 Speak", font=("Arial", 10, "bold"), command=recognize_speech)
voice_button.grid(row=0, column=0, padx=5, pady=5)

save_button = tk.Button(control_frame, text="Save History", font=("Arial", 10, "bold"), command=save_history)
save_button.grid(row=0, column=1, padx=5, pady=5)

summary_button = tk.Button(control_frame, text="Summarize", font=("Arial", 10, "bold"), command=summarize_debate)
summary_button.grid(row=0, column=2, padx=5, pady=5)

exit_button = tk.Button(control_frame, text="Exit", font=("Arial", 10, "bold"), command=root.quit)
exit_button.grid(row=0, column=3, padx=5, pady=5)

# --- Theme ---
style = ttk.Style()
style.theme_use("vista")

# --- Start Main Loop ---
root.mainloop()

import tkinter as tk
from tkinter import scrolledtext, ttk
from debate import debate_with_ai, save_history, summarize_debate, speak_text
import speech_recognition as sr  # Import speech_recognition module
import threading

def setup_gui():
    root = tk.Tk()
    root.title("AI Debate Partner")
    root.geometry("600x700")

    # Debate mode setup
    mode_label = tk.Label(root, text="Select Debate Mode:", font=("Arial", 12, "bold"))
    mode_label.pack(pady=5)
    mode_var = tk.StringVar()
    mode_var.set("Casual Debate")
    modes = ["Formal Debate", "Casual Debate", "Devil’s Advocate"]
    mode_dropdown = ttk.Combobox(root, textvariable=mode_var, values=modes, state="readonly")
    mode_dropdown.pack(pady=5)

    # Buttons and chatbox
    start_button = tk.Button(root, text="Start Debate", font=("Arial", 10, "bold"))
    start_button.pack(pady=5)
    
    chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED)
    chatbox.pack(pady=10)
    
    chatbox.tag_configure("user", foreground="blue", font=("Arial", 11, "bold"))
    chatbox.tag_configure("ai", foreground="green", font=("Arial", 11, "bold"))

    user_input = tk.Entry(root, width=60, font=("Arial", 11))
    user_input.pack(pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    send_button = tk.Button(button_frame, text="Send", font=("Arial", 10, "bold"))
    send_button.grid(row=0, column=0, padx=5)
    voice_button = tk.Button(button_frame, text="🎤 Speak", font=("Arial", 10, "bold"))
    voice_button.grid(row=0, column=1, padx=5)
    save_button = tk.Button(button_frame, text="Save History", font=("Arial", 10, "bold"))
    save_button.grid(row=0, column=2, padx=5)
    
    summary_button = tk.Button(root, text="Summarize", font=("Arial", 10, "bold"))
    summary_button.pack(pady=5)
    exit_button = tk.Button(root, text="Exit", font=("Arial", 10, "bold"))
    exit_button.pack(pady=5)

    return root, chatbox, user_input, send_button, voice_button, save_button, summary_button

def start_debate(mode_var, chatbox, send_message):
    global debate_mode
    debate_mode = mode_var.get()
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n🤖 AI: Let's have a '{debate_mode}' debate. What’s your argument?\n", "ai")
    chatbox.config(state=tk.DISABLED)

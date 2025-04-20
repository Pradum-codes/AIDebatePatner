import tkinter as tk
from gui import setup_gui, start_debate
from debate import debate_with_ai, save_history, summarize_debate
from speech_recog import recognize_speech
import datetime
import debate as db
import config

def send_message(text):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")  # Fixed here
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n🧑‍💼 You [{timestamp}]: {text}\n", "user")
    response = debate_with_ai(text)
    chatbox.insert(tk.END, f"\n🤖 AI [{timestamp}]: {response}\n", "ai")
    db.debate_history.append(f"You [{timestamp}]: {text}\nAI [{timestamp}]: {response}\n")
    chatbox.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)
    db.speak_text(response)


if __name__ == "__main__":
    root, chatbox, user_input, send_button, voice_button, save_button, summary_button = setup_gui()

    # Hook up callbacks
    send_button.config(command=lambda: send_message(user_input.get().strip()))
    voice_button.config(command=lambda: recognize_speech(chatbox, user_input, send_message))
    summary_button.config(command=lambda: summarize_debate())

    root.mainloop()

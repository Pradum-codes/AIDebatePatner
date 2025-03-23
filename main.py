import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime

# Set up Gemini API Key
genai.configure(api_key="")

# Global Variables
debate_history = []  # Stores conversation history
debate_mode = "Casual Debate"

# Function to get AI response
def debate_with_ai(user_input):
    global debate_history

    prompt = f"You are an AI debate partner. We are having a '{debate_mode}' debate.\n\n"
    prompt += f"User: {user_input}\nAI:"

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=300,
            temperature=0.7
        )
    )

    ai_response = response.text if response else "I'm not sure how to respond."
    debate_history.append(f"User: {user_input}\nAI: {ai_response}\n")  # Save to history

    return ai_response

# Function to start debate
def start_debate():
    global debate_mode
    debate_mode = mode_var.get()
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n🤖 AI: Let's have a '{debate_mode}' debate. What’s your argument?\n", "ai")
    chatbox.config(state=tk.DISABLED)

# Function to handle user input
def send_message():
    global debate_history

    user_text = user_input.get().strip()
    if not user_text:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")

    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n🧑‍💼 You [{timestamp}]: {user_text}\n", "user")

    response = debate_with_ai(user_text)
    chatbox.insert(tk.END, f"\n🤖 AI [{timestamp}]: {response}\n", "ai")

    debate_history.append(f"You [{timestamp}]: {user_text}\nAI [{timestamp}]: {response}\n")  # Save to history

    chatbox.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)

# Function to save debate history
def save_history():
    filename = f"Debate_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(debate_history)

    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"\n📜 History saved as '{filename}'\n", "ai")
    chatbox.config(state=tk.DISABLED)

# Function to summarize debate
def summarize_debate():
    global debate_history

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

# GUI Setup
root = tk.Tk()
root.title("AI Debate Partner")
root.geometry("600x650")

# Dropdown for debate modes
mode_label = tk.Label(root, text="Select Debate Mode:", font=("Arial", 12, "bold"))
mode_label.pack(pady=5)

mode_var = tk.StringVar()
mode_var.set("Casual Debate")  # Default mode

modes = ["Formal Debate", "Casual Debate", "Devil’s Advocate"]
mode_dropdown = ttk.Combobox(root, textvariable=mode_var, values=modes, state="readonly")
mode_dropdown.pack(pady=5)

# Start Debate Button
start_button = tk.Button(root, text="Start Debate", font=("Arial", 10, "bold"), command=start_debate)
start_button.pack(pady=5)

# Chatbox with text formatting
chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED)
chatbox.pack(pady=10)

# Text Formatting
chatbox.tag_configure("user", foreground="blue", font=("Arial", 11, "bold"))
chatbox.tag_configure("ai", foreground="green", font=("Arial", 11, "bold"))

# User Input Field
user_input = tk.Entry(root, width=60, font=("Arial", 11))
user_input.pack(pady=5)

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Send Button
send_button = tk.Button(button_frame, text="Send", font=("Arial", 10, "bold"), command=send_message)
send_button.grid(row=0, column=0, padx=5)

# Save History Button
save_button = tk.Button(button_frame, text="Save History", font=("Arial", 10, "bold"), command=save_history)
save_button.grid(row=0, column=1, padx=5)

# Summarize Button
summary_button = tk.Button(button_frame, text="Summarize", font=("Arial", 10, "bold"), command=summarize_debate)
summary_button.grid(row=0, column=2, padx=5)

# Exit Button
exit_button = tk.Button(root, text="Exit", font=("Arial", 10, "bold"), command=root.quit)
exit_button.pack(pady=5)

# Run GUI
root.mainloop()

import google.generativeai as genai
from datetime import datetime
import threading
import pyttsx3

# Global Variables
debate_history = []  # Stores conversation history
context = []  # Context awareness (last 5 exchanges)
debate_mode = "Casual Debate"

def speak_text(text):
    def run():
        local_engine = pyttsx3.init()  # Initialize engine inside thread
        local_engine.say(text)
        local_engine.runAndWait()
        local_engine.stop()  # Stop properly
    threading.Thread(target=run, daemon=True).start()

def debate_with_ai(user_input):
    global context
    context.append(f"User: {user_input}")
    if len(context) > 5:
        context.pop(0)
    
    prompt = f"You are an AI debate partner. We are having a '{debate_mode}' debate.\n\n" + "\n".join(context) + "\nAI:"
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=300,
            temperature=0.7
        )
    )
    ai_response = response.text if response else "I'm not sure how to respond."
    context.append(f"AI: {ai_response}")
    debate_history.append(f"User: {user_input}\nAI: {ai_response}\n")
    return ai_response

def save_history():
    filename = f"Debate_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(debate_history)
    return filename

def summarize_debate():
    if not debate_history:
        return "⚠️ No debate history to summarize."
    
    summary_prompt = "Summarize the following debate:\n\n" + "".join(debate_history)
    model = genai.GenerativeModel("gemini-1.5-flash")
    summary_response = model.generate_content(
        summary_prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=200,
            temperature=0.5
        )
    )
    return summary_response.text if summary_response else "Couldn't generate a summary."

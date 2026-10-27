import json
import re
import sys
from unicodedata import name

def load_faq_data(filename="sample_faq.json"):
    """Loads FAQ and greeting data from the JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Warning: '{filename}' not found. Using fallback default data.")
        return {
            "greetings": ["hello", "hi", "hey", "good morning", "good afternoon"],
            "faqs": [
                {
                    "question": "What are your hours of operation?",
                    "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST."
                },
                {
                    "question": "How do I submit my internship project?",
                    "answer": "You can submit your public GitHub repository link through your Student Workspace."
                },
                {
                    "question": "When will I receive my certificate?",
                    "answer": "Certificates are reviewed and issued within 3-5 business days after your code review."
                }
            ]
        }

def chatbot_assistant():
    print("=" * 65)
    print("      RULE-BASED INTERACTIVE TERMINAL ASSISTANT / CHATBOT      ")
    print("=" * 65)
    print("🤖 Chatbot: Hello! I'm your virtual assistant.")
    print("   You can ask me about our working hours, project submission, certificates,")
    print("   or type 'exit', 'quit', or 'bye' to end the chat.\n")
    
    data = load_faq_data()
    greetings = data.get("greetings", [])
    faqs = data.get("faqs", [])
    
    while True:
        try:
            # User input normalization: lowercase and strip whitespace
            user_input = input("You: ").strip()
            if not user_input:
                continue
                
            # Clean exit commands check
            cleaned_input = user_input.lower()
            exit_commands = ['bye', 'exit', 'quit']
            if cleaned_input in exit_commands or any(re.search(r'\b' + re.escape(cmd) + r'\b', cleaned_input) for cmd in exit_commands):
                print("🤖 Chatbot: Thank you for chatting with me. Have a wonderful day! Goodbye! 👋")
                break
                
            # Check for greetings using regex/keyword matching
            is_greeting = any(re.search(r'\b' + re.escape(g) + r'\b', cleaned_input) for g in greetings)
            if is_greeting:
                print("🤖 Chatbot: Hello there! How can I assist you with your internship today?\n")
                continue
                
            # Intent recognition & matching through keywords against FAQs
            matched_answer = None
            highest_score = 0
            
            # Simple keyword overlap scoring mechanism
            user_words = set(re.findall(r'\w+', cleaned_input))
            
            for faq in faqs:
                q_words = set(re.findall(r'\w+', faq["question"].lower()))
                # Calculate intersection score
                common_words = user_words.intersection(q_words)
                score = len(common_words)
                
                # Boost score if specific key phrases match
                if "hour" in cleaned_input and "hour" in " ".join(q_words):
                    score += 3
                if "submit" in cleaned_input and "submit" in " ".join(q_words):
                    score += 3
                if "certificate" in cleaned_input and "certificate" in " ".join(q_words):
                    score += 3
                    
                if score > highest_score:
                    highest_score = score
                    matched_answer = faq["answer"]
            
            # Response handling based on confidence/score threshold
            if highest_score > 0 and matched_answer:
                print(f"🤖 Chatbot: {matched_answer}\n")
            else:
                # Graceful fallback for unrecognized queries
                print("🤖 Chatbot: I'm sorry, I didn't quite catch that. Could you please rephrase your question or ask about our hours, project submission, or certificates?\n")
                
        except (KeyboardInterrupt, EOFError):
            print("\n🤖 Chatbot: Session interrupted. Goodbye!")
            break

if __name__ == "__main__":
    chatbot_assistant()
# agents/email_agent.py

import re

def process_email(text):
    sender_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    sender = sender_match.group(0) if sender_match else "unknown"
    urgency = "urgent" if "urgent" in text.lower() else "normal"

    return {
        "sender": sender,
        "urgency": urgency,
        "text": text
    }

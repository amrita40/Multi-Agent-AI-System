import json
import mimetypes
import os

from utils.file_utils import extract_text_from_pdf
from agents.audio_agent import transcribe_audio  # Make sure this module exists

def classify_format_and_intent(data, memory, source="unknown"):
    """
    Detects the input format and classifies the intent using rule-based logic.
    Supports PDF, JSON, Email (as string), and Audio (.wav, .mp3) files.
    Logs to shared memory.
    """

    # === FORMAT DETECTION ===
    if isinstance(data, dict):
        format_type = "JSON"
        text = json.dumps(data)

    elif isinstance(data, str) and os.path.exists(data):
        # It's a file path
        if data.endswith(".pdf"):
            format_type = "PDF"
            text = extract_text_from_pdf(data)
        elif data.endswith((".wav", ".mp3")):
            format_type = "Audio"
            text = transcribe_audio(data)
        else:
            format_type = "Unknown"
            text = ""
    
    elif isinstance(data, str) and "@" in data:
        # Probably an email string
        format_type = "Email"
        text = data

    else:
        # Plain text or unknown type
        format_type = "Text"
        text = str(data)

    # === INTENT CLASSIFICATION ===
    lower_text = text.lower()
    if "invoice" in lower_text:
        intent = "Invoice"
    elif "request for quote" in lower_text or "rfq" in lower_text:
        intent = "RFQ"
    elif "complaint" in lower_text:
        intent = "Complaint"
    elif "regulation" in lower_text:
        intent = "Regulation"
    else:
        intent = "Unknown"

    # === LOG TO SHARED MEMORY ===
    memory.log(source, format_type, intent)

    return {
        "source": source,
        "format": format_type,
        "intent": intent,
        "text": text[:300]  # Return first 300 chars for debugging/logs
    }

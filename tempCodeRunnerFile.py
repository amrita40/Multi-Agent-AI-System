import os
import json
import sys
from agents.classifier import classify_format_and_intent
from agents.json_agent import process_json
from agents.email_agent import process_email
from memory.shared_memory import SharedMemory

memory = SharedMemory()

def normalize_filename(filename):
    # Normalize repeated extensions like .wav.wav → .wav
    if filename.endswith('.wav.wav'):
        return filename[:-4]
    if filename.endswith('.pdf.docx'):
        return filename[:-5] + '.pdf'  # if you had .pdf.docx mistakenly, fix to .pdf
    return filename

def load_input(file_path_or_text):
    """
    Load input based on its type:
    - If ends with .json, load and parse JSON.
    - If ends with .pdf, .docx, or .wav, return file path (classifier handles).
    - If path exists, load raw text.
    - Otherwise, treat as raw text string.
    """
    if isinstance(file_path_or_text, str):
        file_path_or_text = normalize_filename(file_path_or_text)
        full_path = os.path.abspath(file_path_or_text)
        print(f"[INFO] Processing: {full_path}")

        if file_path_or_text.endswith('.json'):
            if os.path.isfile(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                raise FileNotFoundError(f"JSON file not found: {full_path}")

        elif file_path_or_text.endswith(('.pdf', '.docx', '.wav')):
            if os.path.isfile(full_path):
                return full_path
            else:
                raise FileNotFoundError(f"Document/audio file not found: {full_path}")

        elif os.path.isfile(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Treat as raw text if no file found
            return file_path_or_text
    else:
        return file_path_or_text

def route_and_process(input_data, source):
    # Classify format and intent
    classification = classify_format_and_intent(input_data, memory, source=source)
    format_ = classification.get("format")
    agent_output = None

    # Route to the correct agent
    if format_ == "JSON":
        agent_output = process_json(classification["text"])
    elif format_ == "Email":
        agent_output = process_email(classification["text"])
    # Add PDF agent routing here if needed

    # Log agent output to shared memory
    memory.log_agent_output(
        source=source,
        format=format_,
        intent=classification.get("intent"),
        agent_output=agent_output,
        timestamp=classification.get("timestamp"),
        thread_id=classification.get("thread_id")
    )

    return {"classification": classification, "agent_output": agent_output}

if __name__ == "__main__":
    print("Current Working Directory:", os.getcwd())

    memory = SharedMemory()
    try:
        # Update your inputs here, use correct file names
        inputs = [
            ("alice@company.com", "Hi, this is a Request for Quote (RFQ) from alice@company.com regarding services."),
            ("json.json", "json.json"),
            ("intern.wav", "intern.wav"),
            ("Untitled design.pdf", "Untitled design.pdf"),
        ]

        results = []

        for source, path_or_text in inputs:
            try:
                input_data = load_input(path_or_text)
            except Exception as e:
                print(f"[ERROR] Failed to load input from {path_or_text}: {e}", file=sys.stderr)
                continue

            try:
                result = classify_format_and_intent(input_data, memory, source=source)
                results.append(result)
            except Exception as e:
                print(f"[ERROR] Failed to classify input from {source}: {e}", file=sys.stderr)

        for result in results:
            print(result)

    finally:
        memory.close()

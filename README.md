# Flowbit-AI-internship# Multi-Agent AI Document & Email Classifier

## Overview

This project is a multi-agent AI system designed to intelligently process and classify incoming business documents in various formats (PDF, JSON, Email/text). The system automatically detects the format and intent of each input, routes it to the appropriate specialized agent, and maintains a shared context for traceability and chaining.

---
## Demo

Here’s a screenshot of the system in action:


## Demo

### Screenshot

![Output Screenshot]()

### Video

!-- Failed to upload "Screen Recording 2025-05-29 023808.mp4" 



## Features

- **Automatic Format & Intent Classification:**  
  Detects if input is a PDF, JSON, or Email, and classifies its business intent (e.g., Invoice, RFQ, Complaint, Regulation).

- **Agent-Based Processing:**  
  - **JSON Agent:** Extracts and reformats structured data, flags anomalies or missing fields.
  - **Email Agent:** Extracts sender, intent, urgency, and formats for CRM-style usage.
  - *(PDF Agent can be added similarly.)*

- **Shared Memory Module:**  
  Uses SQLite for lightweight, persistent storage of:
  - Source, type, timestamp
  - Extracted values
  - Thread/conversation ID
  - Agent outputs for full traceability

- **Extensible Architecture:**  
  Easily add new agents for other formats or business processes.

---

## Example Flow

1. **User sends an email or uploads a file.**
2. **Classifier Agent** detects format and intent (e.g., "Email + RFQ").
3. **Routed to Email Agent**, which extracts sender, urgency, and relevant fields.
4. **Shared Memory** logs all steps, extracted data, and maintains context for future chaining.

---

## Tech Stack

- **Python 3.8+**
- **SQLite** (for shared memory)
- **Modular agent architecture**
- *(Optional: LLMs such as OpenAI GPT for advanced intent extraction)*

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multi-agent-ai-classifier.git
cd multi-agent-ai-classifier
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Project Structure

```
intern project/
├── agents/
│   ├── classifier.py
│   ├── json_agent.py
│   └── email_agent.py
├── memory/
│   └── shared_memory.py
├── main.py
├── shared_memory.db
└── README.md
```

### 4. Run the System

Edit the `inputs` list in `main.py` to point to your test files or email text, then:

```bash
python main.py
```

---

## How It Works

- **main.py**: Entry point. Loads input, classifies, routes, and logs results.
- **agents/classifier.py**: Classifies input format and intent.
- **agents/json_agent.py**: Processes structured JSON.
- **agents/email_agent.py**: Processes email content.
- **memory/shared_memory.py**: Handles persistent logging and context.

---

## Customization

- **Add a PDF Agent:**  
  Implement `agents/pdf_agent.py` and update routing in `main.py`.

- **Integrate LLMs:**  
  Use OpenAI or open-source models for more advanced intent detection.

- **Change Storage:**  
  Swap SQLite for Redis or another backend if needed.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---



## Acknowledgements

- Inspired by real-world business automation needs.
- Built as an internship project.

---

*For questions or support, please open an issue on GitHub.*

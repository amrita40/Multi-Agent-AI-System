# agents/json_agent.py

import json

def process_json(json_string):
    try:
        data = json.loads(json_string)
        anomalies = []

        if isinstance(data, dict):
            records = [data]
        elif isinstance(data, list):
            records = data
        else:
            return {"error": "Unsupported JSON structure"}

        for record in records:
            if "source" not in record or "text" not in record:
                anomalies.append(record)

        return {
            "records_count": len(records),
            "anomalies": anomalies
        }

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON format"
        }

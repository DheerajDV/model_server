import requests
import json

# API endpoint
url = "http://127.0.0.1:8000/predict"

# Sample text for testing (all in one line to avoid JSON formatting issues)
text = "MRF Ltd's shares have seen a decline of over 3% in Friday's trading as two brokerages issue 'Sell' calls. Despite a year-on-year revenue growth of 12% in Q1, MRF's profits fell by 3% due to commodity inflation and higher depreciation costs. Analysts from MOFSL and Kotak Institutional Equities express concerns over MRF's competitive position."

# Request payload
payload = {
    "text": text,
    "labels": ["Company", "Person", "Sector"],
    "threshold": 0.5
}

# Make the request
try:
    response = requests.post(url, json=payload)
    print("\nStatus Code:", response.status_code)
    print("\nDetected Entities:")
    
    if response.status_code == 200:
        entities = response.json()["entities"]
        for entity in entities:
            print(f"\nText: {entity['text']}")
            print(f"Label: {entity['label']}")
            print(f"Position: {entity['start']} to {entity['end']}")
    else:
        print("Error:", response.text)
except Exception as e:
    print("Error connecting to the server:", str(e))

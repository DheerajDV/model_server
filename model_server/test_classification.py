import requests
import json

# API endpoint
url = "http://127.0.0.1:8000/classify"

# Test cases
test_cases = [
    {
        "text": "The company reported strong Q3 earnings with revenue growth of 25% and increased market share",
        "labels": ["bullish", "bearish", "neutral"]
    },
    {
        "text": "Due to rising inflation and weak guidance, the stock dropped 10% after earnings report",
        "labels": ["bullish", "bearish", "neutral"]
    },
    {
        "text": "The market remained stable today with major indices showing minimal movement",
        "labels": ["bullish", "bearish", "neutral"]
    },
    {
        "text": "Tech stocks rally as interest rates stabilize, with NVIDIA hitting new all-time high",
        "labels": ["bullish", "bearish", "neutral"]
    },
    {
        "text": "Oil prices tumble amid global demand concerns, energy sector under pressure",
        "labels": ["bullish", "bearish", "neutral"]
    }
]

# Make requests for each test case
for i, payload in enumerate(test_cases, 1):
    try:
        print(f"\nTest Case {i}:")
        print(f"Text: {payload['text']}")
        print("Labels:", payload['labels'])
        
        response = requests.post(url, json=payload)
        print("\nStatus Code:", response.status_code)
        
        if response.status_code == 200:
            scores = response.json()["scores"]
            print("\nConfidence Scores:")
            # Sort by confidence score
            sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
            for label, score in sorted_scores.items():
                print(f"{label}: {score:.3f}")
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print("Error connecting to the server:", str(e))
    
    print("\n" + "="*50)

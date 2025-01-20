import requests
import json

# API endpoint
url = "http://127.0.0.1:8000/classify"

# Test cases with stock market text
test_cases = [
    {
        "text": "HDFC Bank shows strong growth with Q3 profits surging 30%, analysts upgrade rating citing improved margins and robust credit growth",
        "labels": ["bullish", "bearish", "neutral"]
    },
    {
        "text": "Infosys shares fall 5% as revenue misses estimates, multiple brokerages downgrade stock citing weak guidance and margin pressure",
        "labels": ["bullish", "bearish", "neutral"]
    },
    {
        "text": "TCS maintains steady performance in line with expectations, management sees stable demand environment despite macro uncertainties",
        "labels": ["bullish", "bearish", "neutral"]
    },
    {
        "text": "Reliance Industries sees mixed quarter with retail showing strong growth but O2C margins remain under pressure due to volatile crude prices",
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
            print("\nSentiment Scores:")
            # Sort by confidence score
            sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
            for label, score in sorted_scores.items():
                print(f"{label}: {score:.3f}")
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print("Error connecting to the server:", str(e))
    
    print("\n" + "="*50)

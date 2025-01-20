from gliner import GLiNER
import requests
import json

# Initialize GLiNER with the base model
# model = GLiNER.from_pretrained("urchade/gliner_mediumv2.1")
model = GLiNER.from_pretrained("urchade/gliner_mediumv2.1")

# Sample text for entity prediction
text = """
MRF Ltd's shares have seen a decline of over 3% in Friday's trading as two brokerages issue 'Sell' calls, predicting targets as low as Rs 97,000, indicating a potential 29% downside from current levels.

Despite a year-on-year revenue growth of 12% in Q1, MRF's profits fell by 3% due to commodity inflation and higher depreciation costs.

Analysts from MOFSL and Kotak Institutional Equities express concerns over MRF's competitive position and high stock valuations relative to peers, advocating for a cautious approach in light of rising raw material costs.

Both brokers acknowledged MRF's strong Q1 results amid cost efficiencies but highlight that the rising rubber prices may strain margins moving forward.

While some analysts maintain a positive outlook on market share gains, the consensus is leaning towards a bearish sentiment with revised target prices suggesting significant headwinds ahead for MRF investors..
"""

# Labels for entity prediction
# Most GLiNER models should work best when entity types are in lower case or title case
labels = ["Company", "Person", "Sector"]

# Perform entity prediction
entities = model.predict_entities(text, labels, threshold=0.5)

# Display predicted entities and their labels
for entity in entities:
    print(entity["text"], "=>", entity["label"])

# API endpoint
url = "http://127.0.0.1:8000/predict"

# Test cases
test_cases = [
    {
        "text": "Apple Inc. (AAPL) stock surged 5% after reporting Q4 earnings of $1.5 billion in December 2024. CEO Tim Cook announced new AI initiatives.",
        "labels": ["company", "person", "money", "date", "ticker", "percentage"],
        "threshold": 0.3
    },
    {
        "text": "Microsoft's acquisition of Activision Blizzard for $69 billion was approved by FTC in January 2024, boosting MSFT shares by 3.2%.",
        "labels": ["company", "money", "organization", "date", "ticker", "percentage"],
        "threshold": 0.3
    }
]

# Make requests for each test case
for i, payload in enumerate(test_cases, 1):
    try:
        print(f"\nTest Case {i}:")
        print(f"Text: {payload['text']}")
        print(f"Labels: {payload['labels']}")
        print(f"Threshold: {payload['threshold']}")
        
        response = requests.post(url, json=payload)
        print("\nStatus Code:", response.status_code)
        
        if response.status_code == 200:
            entities = response.json()["entities"]
            print("\nDetected Entities:")
            for entity in entities:
                print(f"{entity['text']} => {entity['label']} (position: {entity['start']}-{entity['end']})")
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print("Error connecting to the server:", str(e))
    
    print("\n" + "="*80)
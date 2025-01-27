import requests
import json
import csv
from collections import defaultdict
import os

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

def classify_announcement(headline, description1="", description2=""):
    """
    Classify BSE announcements into predefined categories
    """
    text = (str(headline) + " " + str(description1) + " " + str(description2)).lower()
    
    # Define keywords for each category
    categories = {
        'Capacity Expansion / New Ventures': ['expansion', 'new venture', 'new plant', 'capacity addition', 'greenfield'],
        'Joint Ventures / Collaborations': ['joint venture', 'collaboration', 'partnership', 'strategic alliance', 'mou'],
        'Order Wins': ['order win', 'contract win', 'project award', 'work order'],
        'Acquisitions': ['acquisition', 'acquire', 'takeover'],
        'USFDA / Regulatory': ['usfda', 'regulatory', 'approval', 'clearance', 'gmp'],
        'Merger / Spin-offs': ['merger', 'demerger', 'spin off', 'amalgamation'],
        'Open Offers / Takeovers': ['open offer', 'takeover offer'],
        'Buyback': ['buyback', 'buy back', 'share repurchase'],
        'Stock Split': ['stock split', 'share split', 'sub-division'],
        'Bonus Issue': ['bonus', 'bonus issue', 'bonus share'],
        'Offer for Sale': ['offer for sale', 'ofs'],
        'Rights Issue': ['rights issue', 'rights offering'],
        'Name Change': ['name change', 'change of name'],
        'Fund Raising': ['fund raising', 'fund raise', 'qip', 'preferential issue', 'rights issue'],
        'First Presentation or Concall': ['earnings call', 'investor presentation', 'concall', 'conference call', 'analyst meet'],
        'Other Important Announcements': []  # Default category
    }
    
    # Check each category
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return 'Other Important Announcements'

def process_announcements(file_path):
    """Process the BSE announcements CSV file"""
    print(f"Processing file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    category_announcements = defaultdict(list)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = 0
            
            for row in reader:
                try:
                    row_count += 1
                    if len(row) < 19:
                        print(f"Row {row_count} has insufficient columns: {len(row)}")
                        continue
                        
                    headline = row[4]  # HEADLINE
                    description1 = row[11] if len(row) > 11 else ""  # DESCRIPTION_1
                    description2 = row[12] if len(row) > 12 else ""  # DESCRIPTION_2
                    company_name = row[18] if len(row) > 18 else ""  # COMPANY_NAME
                    
                    category = classify_announcement(headline, description1, description2)
                    
                    announcement_info = {
                        'company': company_name,
                        'headline': headline,
                        'description': description1 if description1 else description2
                    }
                    
                    category_announcements[category].append(announcement_info)
                    
                except Exception as e:
                    print(f"Error processing row {row_count}: {e}")
                    continue
                    
            print(f"Processed {row_count} rows")
            
    except Exception as e:
        print(f"Error opening file: {e}")
        return {}
    
    return category_announcements

def print_category_details(category_announcements):
    """Print detailed information for each category"""
    if not category_announcements:
        print("No announcements to display")
        return
        
    print("\nDetailed Category Listings:")
    print("=========================")
    
    # Sort categories by number of announcements
    sorted_categories = sorted(
        category_announcements.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    for category, announcements in sorted_categories:
        if len(announcements) > 0:
            print(f"\n{category} ({len(announcements)} announcements):")
            print("=" * (len(category) + 20))
            
            for ann in announcements:
                print(f"\nCompany: {ann['company']}")
                print(f"Announcement: {ann['headline']}")
                if ann['description']:
                    print(f"Details: {ann['description'][:200]}...")

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

if __name__ == "__main__":
    print("Running BSE announcements classification...")
    
    # Use the correct file path
    file_path = "C:/Users/ACER/Desktop/model_server-main/model_server-main/model_server/Jan22_bse_announcements.csv"
    
    print(f"Looking for file: {file_path}")
    
    category_announcements = process_announcements(file_path)
    print_category_details(category_announcements)

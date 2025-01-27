import pandas as pd
import re

def get_combined_text(row):
    """Combine relevant text fields for better classification"""
    headline = str(row['HEADLINE']).lower()
    description = str(row['DESCRIPTION_1']).lower() if pd.notna(row['DESCRIPTION_1']) else ''
    ann_type = str(row['ANNOUNCEMENT_TYPE']).lower() if pd.notna(row['ANNOUNCEMENT_TYPE']) else ''
    return f"{headline} {description} {ann_type}"

def classify_row(row):
    """
    Classify a single announcement row based on its content
    Returns: classification label
    """
    text = get_combined_text(row)
    
    # Define classification patterns
    patterns = {
        'Financial Results': [
            'financial result', 'quarterly result', 'annual result',
            'unaudited financial', 'audited financial', 'financial statement',
            'statement of profit', 'statement of loss'
        ],
        'Board Meeting': [
            'board meeting', 'meeting of board', 'board of director',
            'board meeting intimation'
        ],
        'Shareholder Meeting': [
            'agm', 'annual general meeting', 'egm', 'extraordinary general meeting',
            'postal ballot', 'shareholder meeting', 'general meeting'
        ],
        'Investor Relations': [
            'investor meet', 'analyst meet', 'earnings call', 'investor presentation',
            'investor conference', 'conference call', 'earnings presentation'
        ],
        'Regulatory Compliance': [
            'regulation 30', 'regulation 33', 'sebi regulation', 'compliance certificate',
            'statutory compliance', 'regulatory requirement'
        ],
        'Corporate Action': [
            'dividend', 'bonus', 'stock split', 'rights issue', 'buyback',
            'share transfer', 'capital reduction'
        ],
        'Press Release': [
            'press release', 'media release', 'news release',
            'press statement', 'media statement'
        ],
        'Management Changes': [
            'appointment of director', 'resignation of director',
            'key managerial', 'change in director', 'new appointment'
        ],
        'Trading Update': [
            'trading window', 'insider trading', 'trading update',
            'trading statement', 'market update'
        ],
        'Business Update': [
            'business update', 'operational update', 'company update',
            'corporate update', 'strategic update'
        ],
        'Credit Rating': [
            'credit rating', 'rating agency', 'credit update',
            'rating revision', 'rating reaffirm'
        ],
        'Merger/Acquisition': [
            'merger', 'acquisition', 'amalgamation', 'takeover',
            'scheme of arrangement'
        ]
    }
    
    # Check each pattern
    for category, pattern_list in patterns.items():
        if any(pattern in text for pattern in pattern_list):
            return category
            
    # Special case for board meetings with financial results
    if any(term in text for term in patterns['Board Meeting']):
        if any(term in text for term in patterns['Financial Results']):
            return 'Financial Results - Board Meeting'
    
    # Default category
    return 'Other Announcements'

def main():
    # Read the CSV file
    input_file = "Jan22_bse_announcements_classified.csv"
    df = pd.read_csv(input_file)
    
    # Apply classification to each row
    df['Row_Classification'] = df.apply(classify_row, axis=1)
    
    # Save the classified data
    output_file = "bse_announcements_row_classified.csv"
    df.to_csv(output_file, index=False)
    
    # Print classification summary
    print("\nRow Classification Summary:")
    print("=========================")
    classification_counts = df['Row_Classification'].value_counts()
    total_announcements = len(df)
    
    for category, count in classification_counts.items():
        percentage = (count / total_announcements) * 100
        print(f"{category}: {count} announcements ({percentage:.1f}%)")
    
    # Print examples for each category
    print("\nExample Announcements for Each Category:")
    print("=====================================")
    for category in classification_counts.index:
        examples = df[df['Row_Classification'] == category]['HEADLINE'].head(2)
        print(f"\n{category}:")
        for ex in examples:
            print(f"- {ex}")

if __name__ == "__main__":
    main()

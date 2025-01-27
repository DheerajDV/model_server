import pandas as pd
import json
from collections import defaultdict

def classify_announcements(input_file):
    """
    Classify BSE announcements based on their categories and generate detailed statistics
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Create a dictionary to store announcements by category
    category_announcements = defaultdict(list)
    
    # Process each row
    for _, row in df.iterrows():
        announcement = {
            'company': row['COMPANY_NAME'],
            'headline': row['HEADLINE'],
            'description': row['DESCRIPTION_1'] if pd.notna(row['DESCRIPTION_1']) else '',
            'date': row['DT'],
            'announcement_type': row['ANNOUNCEMENT_TYPE'] if pd.notna(row['ANNOUNCEMENT_TYPE']) else ''
        }
        
        # Add to appropriate category
        category = row['CATEGORY'] if pd.notna(row['CATEGORY']) else 'Uncategorized'
        category_announcements[category].append(announcement)
    
    return category_announcements

def print_classification_summary(category_announcements):
    """Print a summary of the classification results"""
    print("\nBSE Announcements Classification Summary:")
    print("======================================")
    
    # Sort categories by number of announcements
    sorted_categories = sorted(
        category_announcements.items(),
        key=lambda x: len(x[1]),
        reverse=True
    # Descending order by number of announcements
    )
    
    # Print summary
    for category, announcements in sorted_categories:
        print(f"{category}: {len(announcements)} announcements")

def main():
    input_file = "Jan22_bse_announcements_classified.csv"
    
    try:
        # Classify announcements
        category_announcements = classify_announcements(input_file)
        
        # Print classification summary
        print_classification_summary(category_announcements)
        
        # Save detailed results
        output_file = "bse_classification_results.txt"
        save_category_details(category_announcements, output_file)
        
    except Exception as e:
        print(f"Error processing announcements: {str(e)}")

if __name__ == "__main__":
    main()

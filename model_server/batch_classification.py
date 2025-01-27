import pandas as pd
import os
from datetime import datetime
import json
from pathlib import Path

class BSEAnnouncementClassifier:
    def __init__(self):
        self.patterns = {
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
        
    def get_combined_text(self, row):
        """Combine relevant text fields for better classification"""
        headline = str(row['HEADLINE']).lower()
        description = str(row['DESCRIPTION_1']).lower() if pd.notna(row['DESCRIPTION_1']) else ''
        ann_type = str(row['ANNOUNCEMENT_TYPE']).lower() if pd.notna(row['ANNOUNCEMENT_TYPE']) else ''
        return f"{headline} {description} {ann_type}"

    def classify_row(self, row):
        """Classify a single announcement"""
        text = self.get_combined_text(row)
        
        # Check each pattern
        for category, pattern_list in self.patterns.items():
            if any(pattern in text for pattern in pattern_list):
                return category
                
        # Special case for board meetings with financial results
        if any(term in text for term in self.patterns['Board Meeting']):
            if any(term in text for term in self.patterns['Financial Results']):
                return 'Financial Results - Board Meeting'
        
        return 'Other Announcements'

    def process_file(self, input_file, output_dir=None):
        """Process a single file"""
        try:
            df = pd.read_csv(input_file)
            df['Row_Classification'] = df.apply(self.classify_row, axis=1)
            
            # Generate statistics
            stats = self.generate_statistics(df)
            
            # Save results
            if output_dir:
                self.save_results(df, stats, input_file, output_dir)
            
            return df, stats
            
        except Exception as e:
            print(f"Error processing file {input_file}: {str(e)}")
            return None, None

    def process_batch(self, input_dir, output_dir):
        """Process multiple files in batch mode"""
        results = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Process all CSV files in the input directory
        for file in os.listdir(input_dir):
            if file.endswith('.csv'):
                input_file = os.path.join(input_dir, file)
                df, stats = self.process_file(input_file, output_dir)
                if df is not None:
                    results.append({
                        'file': file,
                        'statistics': stats
                    })
        
        # Save batch summary
        self.save_batch_summary(results, output_dir)
        return results

    def generate_statistics(self, df):
        """Generate statistics for the classification results"""
        total_announcements = len(df)
        classification_counts = df['Row_Classification'].value_counts()
        
        stats = {
            'total_announcements': total_announcements,
            'categories': {}
        }
        
        for category, count in classification_counts.items():
            percentage = (count / total_announcements) * 100
            stats['categories'][category] = {
                'count': int(count),
                'percentage': round(percentage, 2)
            }
        
        return stats

    def save_results(self, df, stats, input_file, output_dir):
        """Save classification results and statistics"""
        # Create timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = Path(input_file).stem
        
        # Save classified data
        output_csv = os.path.join(output_dir, f"{base_name}_classified_{timestamp}.csv")
        df.to_csv(output_csv, index=False)
        
        # Save statistics
        stats_file = os.path.join(output_dir, f"{base_name}_stats_{timestamp}.json")
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=4)

    def save_batch_summary(self, results, output_dir):
        """Save summary of batch processing"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_file = os.path.join(output_dir, f"batch_summary_{timestamp}.json")
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=4)

def main():
    # Initialize classifier
    classifier = BSEAnnouncementClassifier()
    
    # Test single file mode
    print("\nTesting Single File Mode:")
    print("========================")
    input_file = "Jan22_bse_announcements_classified.csv"
    output_dir = "classification_results"
    df, stats = classifier.process_file(input_file, output_dir)
    
    if stats:
        print("\nClassification Summary:")
        print("=====================")
        for category, data in stats['categories'].items():
            print(f"{category}: {data['count']} announcements ({data['percentage']}%)")
    
    # Test batch mode
    print("\nTesting Batch Mode:")
    print("=================")
    input_dir = "."  # Current directory
    batch_results = classifier.process_batch(input_dir, output_dir)
    
    print("\nBatch Processing Summary:")
    print("======================")
    for result in batch_results:
        print(f"\nFile: {result['file']}")
        for category, data in result['statistics']['categories'].items():
            print(f"{category}: {data['count']} announcements ({data['percentage']}%)")

if __name__ == "__main__":
    main()

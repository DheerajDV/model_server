import pandas as pd
import os
from datetime import datetime
import json
from pathlib import Path

class BSEAnnouncementClassifier:
    def __init__(self):
        self.required_columns = ['HEADLINE', 'DESCRIPTION_1', 'ANNOUNCEMENT_TYPE', 'COMPANY_NAME', 'DT']
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
        
    def validate_file(self, df):
        """Validate if the DataFrame has required columns"""
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        return True
        
    def get_combined_text(self, row):
        """Combine relevant text fields for better classification"""
        headline = str(row['HEADLINE']).lower()
        description = str(row['DESCRIPTION_1']).lower() if pd.notna(row['DESCRIPTION_1']) else ''
        ann_type = str(row['ANNOUNCEMENT_TYPE']).lower() if pd.notna(row['ANNOUNCEMENT_TYPE']) else ''
        return f"{headline} {description} {ann_type}"

    def classify_row(self, row):
        """Classify a single announcement"""
        start_time = datetime.now()
        
        text = self.get_combined_text(row)
        
        # Check each pattern
        for category, pattern_list in self.patterns.items():
            if any(pattern in text for pattern in pattern_list):
                end_time = datetime.now()
                classification_time = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds
                return category, classification_time
                
        # Special case for board meetings with financial results
        if any(term in text for term in self.patterns['Board Meeting']):
            if any(term in text for term in self.patterns['Financial Results']):
                end_time = datetime.now()
                classification_time = (end_time - start_time).total_seconds() * 1000
                return 'Financial Results - Board Meeting', classification_time
        
        end_time = datetime.now()
        classification_time = (end_time - start_time).total_seconds() * 1000
        return 'Other Announcements', classification_time

    def process_file(self, input_file, output_dir=None):
        """Process a single file"""
        try:
            print(f"\nProcessing file: {input_file}")
            print("=" * 50)
            df = pd.read_csv(input_file)
            
            # Validate file format
            self.validate_file(df)
            
            print("\nClassifying announcements...")
            # Track classification times
            classification_times = []
            classifications = []
            
            # Classify each row and track time
            total_rows = len(df)
            for idx, row in df.iterrows():
                classification, time_taken = self.classify_row(row)
                classifications.append(classification)
                classification_times.append(time_taken)
            
            df['Row_Classification'] = classifications
            
            # Calculate and display timing statistics
            avg_time = sum(classification_times) / len(classification_times)
            max_time = max(classification_times)
            min_time = min(classification_times)
            total_time = sum(classification_times)
            
            print("\nClassification Timing Statistics:")
            print("-" * 30)
            print(f"Total rows processed: {total_rows}")
            print(f"Total classification time: {total_time:.2f} ms ({total_time/1000:.2f} seconds)")
            print(f"Average time per row: {avg_time:.2f} ms")
            print(f"Maximum time for a row: {max_time:.2f} ms")
            print(f"Minimum time for a row: {min_time:.2f} ms")
            print("-" * 30)
            
            # Generate statistics
            stats = self.generate_statistics(df)
            
            # Save results
            if output_dir:
                self.save_results(df, stats, input_file, output_dir)
            
            return df, stats
            
        except ValueError as ve:
            print(f"Error processing file {input_file}: {str(ve)}")
            return None, None
        except Exception as e:
            print(f"Unexpected error processing file {input_file}: {str(e)}")
            return None, None

    def process_batch(self, input_dir, output_dir):
        """Process multiple files in batch mode"""
        results = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Process all CSV files in the input directory
        csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        print(f"\nFound {len(csv_files)} CSV files to process")
        
        for file in csv_files:
            input_file = os.path.join(input_dir, file)
            df, stats = self.process_file(input_file, output_dir)
            if df is not None:
                results.append({
                    'file': file,
                    'statistics': stats
                })
        
        # Save batch summary
        if results:
            self.save_batch_summary(results, output_dir)
            print(f"\nSuccessfully processed {len(results)} files")
        else:
            print("\nNo files were successfully processed")
            
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
        print(f"Saved classified data to: {output_csv}")
        
        # Save statistics
        stats_file = os.path.join(output_dir, f"{base_name}_stats_{timestamp}.json")
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=4)
        print(f"Saved statistics to: {stats_file}")

    def save_batch_summary(self, results, output_dir):
        """Save summary of batch processing"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_file = os.path.join(output_dir, f"batch_summary_{timestamp}.json")
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Saved batch summary to: {summary_file}")

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
    
    if batch_results:
        print("\nBatch Processing Summary:")
        print("======================")
        for result in batch_results:
            print(f"\nFile: {result['file']}")
            for category, data in result['statistics']['categories'].items():
                print(f"{category}: {data['count']} announcements ({data['percentage']}%)")

if __name__ == "__main__":
    main()

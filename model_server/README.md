# Stock Market Sentiment Analysis API

A FastAPI-based service that provides two main functionalities:
1. Named Entity Recognition (NER) using modern-GLiNER-large model
2. Stock Market Sentiment Analysis (Bullish/Bearish/Neutral classification)

## Features

- **NER Endpoint** (`/predict`):
  - Uses knowledgator/modern-gliner-bi-large-v1.0 model for state-of-the-art named entity recognition
  - Configurable confidence threshold
  - Returns entities with their positions in text

- **Sentiment Analysis Endpoint** (`/classify`):
  - Analyzes stock market related text
  - Returns confidence scores for bullish, bearish, and neutral sentiments
  - Optimized for financial market context

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd model_server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required models:
```bash
python download_models.py
```

## Usage

1. Start the server:
```bash
python -m uvicorn main:app --reload
```

2. The API will be available at `http://127.0.0.1:8000`

3. API Endpoints:
   - Swagger UI Documentation: `http://127.0.0.1:8000/docs`
   - NER: `POST /predict`
   - Sentiment Analysis: `POST /classify`

### Example Request (Sentiment Analysis)

```python
import requests

url = "http://127.0.0.1:8000/classify"
payload = {
    "text": "The company reported strong Q3 earnings with revenue growth of 25%",
    "labels": ["bullish", "bearish", "neutral"]
}

response = requests.post(url, json=payload)
print(response.json())
```

## Docker Support

Build and run the application using Docker:

```bash
docker build -t model-server .
docker run -p 8000:8000 model-server
```

## Testing

The project includes comprehensive test suites:

```bash
# Run all tests
python -m pytest

# Individual test files
python test_classification.py  # Sentiment analysis tests
python test_gliner.py         # GLiNER model tests
python test_api.py            # API endpoint tests
python test_stock_sentiment.py # Stock sentiment tests
```

## Requirements

Key dependencies:
- fastapi
- uvicorn
- gliner==0.1.3
- requests
- numpy
- pydantic

For a complete list of dependencies, see `requirements.txt`.

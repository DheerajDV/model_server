from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from gliner import GLiNER
from classification_model import TextClassifier

app = FastAPI(title="NLP API", description="API for Named Entity Recognition and Text Classification")

# Add CORS middleware. middleware to FastAPI application. Prcoesses HTTP requests globally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
print("Loading GLiNER model...")
ner_model = GLiNER.from_pretrained("urchade/gliner_mediumv2.1")
classifier = TextClassifier()

# NER Models
class NERRequest(BaseModel):
    text: str
    labels: List[str]
    threshold: float = 0.5 #default threshold

    class Config:
        schema_extra = {
            "example": {
                "text": "MRF Ltd's shares have seen a decline of over 3% in Friday's trading",
                "labels": ["Company", "Person", "Sector"],
                "threshold": 0.5
            }
        }

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int

class NERResponse(BaseModel):
    entities: List[Entity]

# Classification Models
#Input Schema
class ClassificationRequest(BaseModel):
    text: str
    labels: List[str]

    class Config:
        schema_extra = {
            "example": {
                "text": "The customer service was excellent and the staff was very friendly",
                "labels": ["positive", "negative", "neutral"]
            }
        }

#Output Schema
class ClassificationResponse(BaseModel):
    scores: Dict[str, float]

@app.post("/predict", response_model=NERResponse)
async def predict_entities(request: NERRequest):
    try:
        entities = ner_model.predict_entities(request.text, request.labels, threshold=request.threshold)
        response_entities = [
            Entity(
                text=entity["text"],
                label=entity["label"],
                start=entity["start"],
                end=entity["end"]
            )
            for entity in entities
        ]
        return NERResponse(entities=response_entities)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# text classification
@app.post("/classify", response_model=ClassificationResponse)
async def classify_text(request: ClassificationRequest):
    try:
        scores = classifier.predict_proba(request.text, request.labels)
        return ClassificationResponse(scores=scores)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add a root endpoint for testing
@app.get("/")
async def root():
    return {"message": "API is running. Use /predict for NER and /classify for text classification."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
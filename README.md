# Transaction Categorizer

A machine learning system for automatically categorizing financial transactions.

## Project Structure

```
transaction_categorizer/
├── api/                    # FastAPI application
│   ├── routes/            # API endpoints
│   └── schemas/           # Pydantic models
├── data/                  # Data directory
│   └── transactions.csv   # Sample transaction data
├── ml/                    # Machine learning code
│   ├── features/         # Feature engineering
│   ├── models/           # Model training
│   └── preprocessing/    # Data preprocessing
├── models/               # Saved models directory
├── scripts/             # Command-line scripts
├── services/            # Business logic
└── utils/               # Utility functions
```

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Training the Model

```bash
python scripts/train.py
```

### Making Predictions

```bash
python scripts/predict.py data/transactions.csv
```

### Running the API

```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /api/v1/categorize`: Categorize a single transaction
- `GET /api/v1/health`: Health check endpoint 
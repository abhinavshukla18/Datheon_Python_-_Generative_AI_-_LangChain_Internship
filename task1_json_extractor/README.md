# Task 1: Structured LLM Prompt Pipeline & JSON Extractor

Extracts structured data from unstructured invoice text using the Gemini API, with output validated by Pydantic.

## Features
- Parameterized prompt template with a few-shot example
- Gemini structured output (JSON schema) plus Pydantic validation
- Automatic retry if validation fails
- Batch runner that processes every invoice in `sample_invoices/`

## Setup
```
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and add your Gemini API key.

## Usage
Single invoice:
```
python extract.py sample_invoices/invoice1.txt
```
All sample invoices (saves JSON to `output/`):
```
python run_all.py
```

## Project structure
- `schemas.py` - Pydantic models (`Invoice`, `LineItem`)
- `extract.py` - prompt template, API call, validation and retry
- `run_all.py` - batch processing
- `sample_invoices/` - messy sample inputs in different formats
- `output/` - extracted JSON results

## Tech
Python 3, google-genai, Pydantic, python-dotenv
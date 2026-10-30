import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from schemas import Invoice

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),
)

MODEL = "gemini-flash-lite-latest"
MAX_RETRIES = 3

PROMPT_TEMPLATE = """You are an invoice data extraction system.
Extract the fields from the invoice text and return JSON only.

Rules:
- Dates must be in YYYY-MM-DD format.
- Amounts must be plain numbers without currency symbols.
- Currency must be a 3-letter code (for example INR, USD).
- If a field is missing, use an empty string or 0.

Example input:
{example_input}

Example output:
{example_output}

Now extract from this invoice:
{document_text}
"""

EXAMPLE_INPUT = """INVOICE #A-77
Date: 3 March 2026
From: Sunrise Traders
Bill to: Ravi Kumar
Items:
- Rice Bag 10kg x 2 @ Rs 800 each
- Cooking Oil 1L x 1 @ Rs 150
Total: Rs 1750"""

EXAMPLE_OUTPUT = """{"invoice_number": "A-77", "invoice_date": "2026-03-03", "vendor_name": "Sunrise Traders", "customer_name": "Ravi Kumar", "items": [{"description": "Rice Bag 10kg", "quantity": 2, "unit_price": 800.0}, {"description": "Cooking Oil 1L", "quantity": 1, "unit_price": 150.0}], "total_amount": 1750.0, "currency": "INR"}"""


def extract_invoice(document_text):
    prompt = PROMPT_TEMPLATE.format(
        example_input=EXAMPLE_INPUT,
        example_output=EXAMPLE_OUTPUT,
        document_text=document_text,
    )
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Invoice,
                    temperature=0,
                ),
            )
            return Invoice.model_validate_json(response.text)
        except ValidationError as e:
            last_error = e
            print(f"Attempt {attempt} failed validation, retrying...")
    raise RuntimeError(f"Extraction failed after {MAX_RETRIES} attempts: {last_error}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_invoices/invoice1.txt"
    with open(path, encoding="utf-8") as f:
        text = f.read()
    invoice = extract_invoice(text)
    print(invoice.model_dump_json(indent=2))
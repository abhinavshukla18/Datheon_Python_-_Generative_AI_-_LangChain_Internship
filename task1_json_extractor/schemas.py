from pydantic import BaseModel


class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float


class Invoice(BaseModel):
    invoice_number: str
    invoice_date: str
    vendor_name: str
    customer_name: str
    items: list[LineItem]
    total_amount: float
    currency: str
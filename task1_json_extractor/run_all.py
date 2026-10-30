import os
from extract import extract_invoice

os.makedirs("output", exist_ok=True)

for name in sorted(os.listdir("sample_invoices")):
    if not name.endswith(".txt"):
        continue
    with open(os.path.join("sample_invoices", name), encoding="utf-8") as f:
        text = f.read()
    try:
        invoice = extract_invoice(text)
        out_path = os.path.join("output", name.replace(".txt", ".json"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(invoice.model_dump_json(indent=2))
        print(f"OK     {name} -> {out_path}")
    except Exception as e:
        print(f"FAILED {name}: {e}")
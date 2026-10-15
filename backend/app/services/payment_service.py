import uuid
import random

def process_payment(amount: float) -> dict:
    reference = f"sim_{uuid.uuid4().hex[:16]}"
    success = random.random() > 0.1
    return {"success": success, "reference": reference}
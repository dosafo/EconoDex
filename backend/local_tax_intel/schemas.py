"""Request/response shapes for local tax + budget intel. Extend as you add data sources."""
from typing import Any

from pydantic import BaseModel


class BillAllocation(BaseModel):
    """One bill's budget allocation (stub shape). TODO: add source, date, amount, category."""
    bill_id: str = ""
    title: str = ""
    category: str = ""
    amount_note: str = ""


class ZipTaxBudgetSummary(BaseModel):
    """Summary for a zip: tax rate + recent bills + proportion breakdown. AI can use this."""
    zip_code: str
    tax_rate_note: str = ""  # TODO: actual rate + source (e.g. state/county)
    recent_bills: list[BillAllocation] = []
    proportion_breakdown: dict[str, Any] = {}  # e.g. {"education": 0.32, "infrastructure": 0.18}
    schema_version: str = "1"

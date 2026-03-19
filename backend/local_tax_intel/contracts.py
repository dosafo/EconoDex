"""Contract and stub for zip → tax rate + bills + budget allocation. Implement incrementally."""
from typing import Protocol

from .schemas import ZipTaxBudgetSummary


class LocalTaxIntelContract(Protocol):
    """Contract: given zip code, return tax rate, recent signed bills (budget allocation), proportion breakdown."""

    def run(self, zip_code: str) -> ZipTaxBudgetSummary:
        ...


def local_tax_intel_stub(zip_code: str) -> ZipTaxBudgetSummary:
    """Stub: returns empty summary. TODO: wire to public bill/tax data sources."""
    return ZipTaxBudgetSummary(
        zip_code=zip_code,
        tax_rate_note="",
        recent_bills=[],
        proportion_breakdown={},
        schema_version="1",
    )

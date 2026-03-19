"""Local Tax & Budget Intel API. Stub endpoint; implement per docs/local_tax_intel_overview.md."""
from fastapi import APIRouter

from backend.local_tax_intel import local_tax_intel_stub
from backend.local_tax_intel.schemas import ZipTaxBudgetSummary

router = APIRouter(prefix="/local-tax-intel", tags=["local-tax-intel"])


@router.get("/zip/{zip_code}", response_model=ZipTaxBudgetSummary)
def get_zip_tax_budget(zip_code: str):
    """Search by zip: tax rate + recent bills (budget allocation) + proportion breakdown. Stub for now."""
    return local_tax_intel_stub(zip_code)

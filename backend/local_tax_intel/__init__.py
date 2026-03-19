"""
Local Tax & Budget Intel: search by zip code, correlate tax rate with recent bills
(budget allocation) so users can see what proportion of their tax dollars likely go where.
Build incrementally; see docs/local_tax_intel_overview.md.
"""
from .contracts import LocalTaxIntelContract, local_tax_intel_stub
from .schemas import ZipTaxBudgetSummary

__all__ = ["LocalTaxIntelContract", "local_tax_intel_stub", "ZipTaxBudgetSummary"]

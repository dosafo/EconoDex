# Local Tax & Budget Intel — Overview

## Goal

Let users search by **zip code** to get:

- **Tax rate** at that zip (e.g. state/county/local).
- **Recent bills signed** that indicate **budget allocation**.
- A **proportion breakdown** (what share of tax dollars likely goes where).

With AI, a user can get a clearer picture of what proportion of their tax dollars are likely going to which areas (education, infrastructure, etc.).

## Where It Lives

| Piece | Location |
|-------|----------|
| Contract + stub | `backend/local_tax_intel/contracts.py` |
| Response schemas | `backend/local_tax_intel/schemas.py` |
| API | `backend/api/local_tax_intel.py` — `GET /api/v1/local-tax-intel/zip/{zip_code}` |

## Contract

- **LocalTaxIntelContract**: `run(zip_code: str) -> ZipTaxBudgetSummary`.
- **ZipTaxBudgetSummary**: `zip_code`, `tax_rate_note`, `recent_bills[]`, `proportion_breakdown`, `schema_version`.

## Implementing Incrementally

1. **Tax rate by zip** — Wire to a public source (e.g. state/county tax data, existing economic hub or adapter). Populate `tax_rate_note` (and add structured fields if you want).
2. **Recent bills / budget allocation** — Add a data source for signed bills and allocations (e.g. government APIs, scrapers). Map to `BillAllocation` and `recent_bills`.
3. **Proportion breakdown** — Derive from allocations (e.g. by category) so users see shares; optional: use AI to summarize.
4. **AI layer** — Consume `ZipTaxBudgetSummary` (e.g. in a separate agent or prompt) to answer user questions about where their tax dollars go.

No extra code was added beyond this scaffolding; extend the stub and schemas as you add sources.

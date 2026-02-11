# Data Storage

This directory contains database schemas, models, and storage configurations.

## Structure

```
data_storage/
├── models/            # SQLAlchemy models
├── schemas/           # Database schemas
├── migrations/        # Database migrations (Alembic)
├── raw_data/          # Raw collected data (gitignored)
└── processed_data/    # Processed data (gitignored)
```

## Implementation Plan

### Phase 1: Labor Market Data Schema
1. Design tables for:
   - Labor market statistics
   - Employment data
   - Unemployment rates
   - Wage data
   - Time series metadata

2. Create SQLAlchemy models
3. Set up Alembic for migrations
4. Create initial migration

## Database Design Considerations

- **Time Series Data**: Efficient storage and querying of time series
- **Data Versioning**: Track data updates and changes
- **Source Attribution**: Link data to original sources
- **Metadata**: Store collection dates, update timestamps, etc.


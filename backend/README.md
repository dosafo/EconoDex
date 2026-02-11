# Backend API

This directory contains the API server and business logic.

## Structure

```
backend/
├── api/               # API routes and endpoints
├── services/          # Business logic services
├── schemas/           # Pydantic schemas for request/response
├── middleware/        # Custom middleware
└── main.py           # Application entry point
```

## Implementation Plan

### Phase 1: Basic API
1. Set up FastAPI/Flask application
2. Create health check endpoint
3. Create data retrieval endpoints
4. Implement basic search functionality
5. Add filtering and pagination

### Phase 2: Advanced Features
- Advanced search with full-text search
- Data aggregation endpoints
- Chart data endpoints
- Export functionality

## API Endpoints (Planned)

- `GET /health` - Health check
- `GET /api/v1/labor-market` - Get labor market data
- `GET /api/v1/labor-market/search` - Search labor market data
- `GET /api/v1/labor-market/stats` - Get statistics
- `GET /api/v1/charts/{chart_id}` - Get chart data


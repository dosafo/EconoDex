# Getting Started with EconoDex

This guide will walk you through setting up and starting development on EconoDex.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher (or SQLite for development)
- Node.js 16+ (for frontend development)
- Git

## Initial Setup

### 1. Clone and Navigate to Project
```bash
cd /Users/dannyosafo/EconoDex
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies (when ready)
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
# Copy example environment file
cp config/.env.example config/.env

# Edit config/.env with your settings
# At minimum, set up database connection
```

### 4. Set Up Database

**Option A: PostgreSQL (for production-like setup)**

If you have PostgreSQL installed:
```bash
# On macOS with Homebrew, you may need to add PostgreSQL to PATH:
export PATH="/usr/local/opt/postgresql@14/bin:$PATH"  # Adjust version as needed
# Or if installed via Homebrew:
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"

# Then create the database:
createdb econodex_db
```

If `createdb` is still not found:
- **Install PostgreSQL**: `brew install postgresql@14` (on macOS)
- **Or use psql directly**: `psql postgres -c "CREATE DATABASE econodex_db;"`
- **Or use SQLite** (see Option B below)

**Option B: SQLite (recommended for development)**

SQLite is simpler and doesn't require a separate database server:
```bash
# No setup needed! SQLite will create the database file automatically
# when you first run your application. Just set DATABASE_URL in .env:
# DATABASE_URL=sqlite:///./econodex.db
```

**Run migrations (when implemented)**
```bash
# alembic upgrade head
```

### 5. Set Up Frontend (When Ready)
```bash
cd frontend
npm install
npm run dev
```

## Development Workflow

### Step 1: Start with Data Collection
1. Research BLS API documentation
2. Get BLS API key (if required)
3. Create `data_collectors/base/collector.py`
4. Create `data_collectors/bls/client.py`
5. Test data collection with sample requests

### Step 2: Set Up Data Storage
1. Design database schema for labor market data
2. Create SQLAlchemy models in `data_storage/models/`
3. Set up Alembic for migrations
4. Create initial migration
5. Test data insertion

### Step 3: Build Data Processing Pipeline
1. Create ETL pipeline in `data_processing/pipelines/`
2. Implement data cleaning functions
3. Test with collected data
4. Set up scheduled processing (optional)

### Step 4: Create Backend API
1. Set up FastAPI/Flask in `backend/`
2. Create first endpoint (health check)
3. Create data retrieval endpoint
4. Test API with sample data

### Step 5: Build Frontend
1. Set up React/Vue project
2. Create basic layout
3. Connect to backend API
4. Create first visualization

## Recommended Development Order

1. **Week 1**: Set up environment, research BLS API, create first data collector
2. **Week 2**: Design database schema, create models, test data storage
3. **Week 3**: Build data processing pipeline, collect sample data
4. **Week 4**: Create basic API, test end-to-end data flow
5. **Week 5+**: Build frontend, add visualizations, iterate

## Testing Your Setup

### Test Data Collection
```bash
# When implemented, run:
python scripts/collect_data.py --source bls --type labor-market
```

### Test API
```bash
# When implemented, run:
python backend/main.py
# Then visit http://localhost:8000/health
```

## Next Steps

1. Read the main [README.md](README.md) for project overview
2. Review the [data_collectors/README.md](data_collectors/README.md) for data collection plan
3. Check [data_storage/README.md](data_storage/README.md) for database design
4. Start implementing based on the plan in each directory's README

## Getting Help

- Review documentation in each directory
- Check API documentation for data sources
- Refer to framework documentation (FastAPI/Flask, React/Vue)

## Tips

- Start small: Get one data source working end-to-end before adding more
- Test frequently: Write tests as you build
- Document as you go: Keep notes on API endpoints, data formats, etc.
- Use version control: Commit frequently with clear messages


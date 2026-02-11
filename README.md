# EconoDex - Economic Data Hub

A comprehensive platform for accessing and visualizing publicly available economic, social, and political data from sources like BLS, polls, surveys, and news articles.

## Project Overview

EconoDex aims to be a centralized hub where users can easily find quantitative data, charts, and statistics on topics like tariffs, immigration, labor markets, and more. The platform will aggregate data from multiple public sources and present it in an accessible, searchable format.

## Current Focus

**Phase 1: Labor Market Data (25 years)**
- Collect and organize labor market data from the past 25 years
- Build foundational data collection and storage infrastructure
- Create basic visualization capabilities
- Expand to 50 years when data is available

## Project Structure

```
EconoDex/
├── data_collectors/      # Scripts for collecting data from various sources
├── data_storage/         # Database schemas and storage configurations
├── data_processing/      # ETL pipelines and data transformation
├── backend/              # API server and business logic
├── frontend/             # Web interface
├── docs/                 # Documentation
├── config/               # Configuration files
├── tests/                # Test suites
└── scripts/              # Utility scripts
```

## Getting Started

### Step 1: Environment Setup
1. Set up Python virtual environment
2. Install dependencies (see `requirements.txt`)
3. Configure environment variables (see `config/.env.example`)
4. Set up database (PostgreSQL recommended)

### Step 2: Data Collection Infrastructure
1. Start with BLS API integration
2. Create data collector base classes
3. Implement labor market data collector
4. Set up data validation and error handling

### Step 3: Data Storage
1. Design database schema for labor market data
2. Set up data models
3. Implement data ingestion pipeline
4. Create data backup and versioning system

### Step 4: Data Processing
1. Create ETL pipelines for raw data
2. Implement data cleaning and normalization
3. Build data aggregation functions
4. Create data quality checks

### Step 5: Backend API
1. Set up API framework (FastAPI/Flask)
2. Create endpoints for data retrieval
3. Implement search functionality
4. Add filtering and pagination

### Step 6: Frontend
1. Set up frontend framework (React/Vue)
2. Create data visualization components
3. Build search interface
4. Implement chart/graph displays

### Step 7: Testing & Deployment
1. Write unit and integration tests
2. Set up CI/CD pipeline
3. Deploy to staging environment
4. Production deployment

## Next Steps (Detailed)

### Immediate Next Steps (Week 1-2)
1. **Research Data Sources**
   - Document BLS API endpoints and data availability
   - Identify other labor market data sources
   - Map out data schemas and formats

2. **Set Up Development Environment**
   - Initialize Python project with virtual environment
   - Install core dependencies (pandas, requests, sqlalchemy)
   - Set up version control (Git)
   - Create initial database schema

3. **Build First Data Collector**
   - Create BLS API client
   - Implement labor market data fetcher
   - Add basic error handling and logging
   - Test with sample data

### Short-term Goals (Month 1)
- Complete BLS labor market data collection
- Store 25 years of historical data
- Create basic data processing pipeline
- Build simple API endpoint to retrieve data
- Create first visualization (basic chart)

### Medium-term Goals (Months 2-3)
- Expand to additional data sources
- Implement search functionality
- Build comprehensive visualization library
- Add data export capabilities
- Create user interface for browsing data

### Long-term Goals (Months 4-6)
- Expand to 50 years of historical data
- Add more data categories (polls, surveys, news)
- Implement advanced analytics
- Add user accounts and saved searches
- Deploy to production

## Technology Stack Recommendations

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI (recommended) or Flask
- **Database**: PostgreSQL (structured data) + Redis (caching)
- **ORM**: SQLAlchemy
- **Data Processing**: Pandas, NumPy

### Frontend
- **Framework**: React or Vue.js
- **Visualization**: D3.js, Chart.js, or Plotly
- **UI Library**: Material-UI or Tailwind CSS

### Data Collection
- **HTTP Client**: Requests or httpx
- **Web Scraping**: BeautifulSoup, Scrapy (if needed)
- **API Clients**: Custom clients for BLS, etc.

### Infrastructure
- **Containerization**: Docker
- **Deployment**: AWS, GCP, or Heroku
- **Monitoring**: Logging and error tracking

## Data Sources to Explore

1. **Bureau of Labor Statistics (BLS)**
   - Employment statistics
   - Unemployment rates
   - Wage data
   - Occupational data

2. **Federal Reserve Economic Data (FRED)**
   - Economic indicators
   - Labor market metrics

3. **Census Bureau**
   - Demographic data
   - Employment surveys

4. **Polls & Surveys**
   - Gallup
   - Pew Research
   - Other polling organizations

5. **News Articles**
   - News APIs (NewsAPI, etc.)
   - RSS feeds

## Development Principles

1. **Incremental Development**: Build and test one feature at a time
2. **Data Quality First**: Ensure data accuracy and reliability
3. **Documentation**: Keep documentation up to date
4. **Testing**: Write tests as you build
5. **Version Control**: Commit frequently with clear messages

## Contributing

This is currently a personal project, but contributions and suggestions are welcome!

## License

[To be determined]


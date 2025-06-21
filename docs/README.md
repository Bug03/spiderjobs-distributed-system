# SpiderJobs Documentation

This folder contains all documentation for the SpiderJobs distributed crawler system.

## Documents

- **[PHASE1_SUMMARY.md](PHASE1_SUMMARY.md)** - Complete summary of Phase 1 implementation with test results and performance metrics

## Phase 1 Architecture

### Core Components

1. **Main Crawler (`crawler.py`)**

   - Entry point with CLI interface
   - Handles pagination and search queries
   - Manages HTTP requests with retry logic
   - Exports data to CSV format

2. **Parser Module (`parsers/`)**

   - `itviec.py` - ITviec-specific job parsing logic
   - Adapter pattern for easy extension to new sites
   - Robust field extraction with multiple fallback strategies

3. **Configuration (`config.py`)**
   - Centralized settings for all components
   - Site-specific configurations
   - Output and database settings

### Data Flow

```
ITviec.com → HTTP Request → HTML Parser → JobListing Objects → CSV Export
```

### Job Data Schema

```python
@dataclass
class JobListing:
    title: str          # Job title
    link: str           # Full URL to job posting
    company: str        # Company name
    location: str       # Job location
    posted_date: str    # When job was posted
    logo_url: str       # Company logo URL
    skills: List[str]   # List of technologies/skills
```

## Usage Patterns

### Basic Usage

```bash
python crawler.py                    # Crawl 3 pages, save to outputs/itviec_jobs.csv
python crawler.py --pages 5          # Crawl 5 pages
python test_crawler.py               # Quick test
python demo.py                       # Full feature demonstration
```

### Advanced Usage

```bash
python crawler.py --pages 10 --query "python developer" --output outputs/python_jobs.csv --delay 2.0
```

## Performance Characteristics

- **Throughput**: ~22 jobs per page in 1-2 seconds
- **Success Rate**: 100% for tested pages
- **Memory Usage**: Minimal - processes pages individually
- **Network Politeness**: Configurable delays (default 1.0s)

## Extensibility

The system is designed for easy extension:

1. **New Sites**: Add new parser classes in `parsers/` folder
2. **New Data Fields**: Extend `JobListing` dataclass
3. **New Output Formats**: Add methods to crawler class
4. **New Storage**: Implement database adapters

## Next Phase

Phase 2 will implement:

- Redis-based URL frontier
- Worker-based distributed crawling
- Additional job sites (TopDev, VietnamWorks)
- Deduplication service
- Real-time monitoring

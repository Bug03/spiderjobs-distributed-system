# SpiderJobs - Distributed Crawler System

Distributed Web Crawler System for aggregating job listings across multiple sites (ITviec, TopDev, VietnamWorks...).

## High Level Worker Crawler Diagram

![Worker Crawler Architecture](https://www.educative.io/api/collection/10370001/4941429335392256/page/4695113376989184/image/5582955482578944?page_type=collection_lesson&get_optimised=true&collection_token=undefined)

---

## Problem Definition

Current issue: There are too many job listing websites. It is difficult and time-consuming for users to check hundreds of jobs daily, across multiple sites, and filter suitable opportunities.

Goal: Build a distributed web crawler system to automatically collect job data from multiple websites, aggregate it into a single database, and provide an API or UI for easy search and notification.

---

## Functional Requirements

- Crawl job listings from multiple sites (ITviec, TopDev, VietnamWorks...)
- Parse essential fields: title, link, company, location, posted date, salary, logo
- Handle site pagination
- Deduplicate job listings
- Store results in MongoDB / CSV / ElasticSearch
- Provide search API / UI for users
- Support regular crawling (daily, hourly)
- Monitoring and alerting (crawl rate, error rate)

---

## Non-Functional Requirements

- Scalable: able to crawl 10k-100k pages/day
- Fault tolerant: handle retries, errors, site blocks
- Maintainable: easy to add new sites / update parsers
- Low cost: suitable for small team (\~\$50-70/month infra)
- Observability: real-time monitoring and alerting
- Politeness: respect site rate limits and avoid bans

---

## Core Entities

| Entity       | Description                         |
| ------------ | ----------------------------------- |
| JobListing   | Parsed job data (title, link, etc.) |
| URL Frontier | Queue of URLs to crawl              |
| SiteConfig   | Per-site parsing and rate config    |
| CrawlLog     | Record of crawl results and errors  |
| ProxyPool    | List of proxies for rotating IPs    |

---

## Input / Output

**Input:**

- Seed URLs (ITviec, TopDev, VietnamWorks)
- Site-specific config (selectors, rate limit)

**Output:**

- Parsed JobListing data → MongoDB / CSV / ElasticSearch
- Logs → Prometheus / Grafana

---

## Tasklist by Phases

### Phase 1: MVP Crawler (2 weeks)

- [x] Setup Git repo for crawler project
- [x] Implement single-site crawler (ITviec)

  - [x] Fetch HTML page
  - [x] Parse: title, link, company, location, posted date, logo
  - [x] Save to CSV / MongoDB

- [x] Handle pagination (crawl multiple pages)
- [x] Implement adapter pattern for Parser

  - [x] ITviecParser

### Phase 2: Queue-based Pipeline (2-3 weeks)

- [ ] Setup Redis (frontier queue)
- [ ] Implement URL producer (Seed URL -> Queue)
- [ ] Build Downloader Worker (consume queue)
- [ ] Implement Politeness (delay / rate-limit)
- [ ] Add Proxy Pool support (basic)
- [ ] Parse multiple sites

  - [ ] Add TopDevParser
  - [ ] Support per-site config

- [ ] Implement Deduplication service

  - [ ] URL hash
  - [ ] Content hash / Bloom Filter

### Phase 3: Monitoring & Stability (2 weeks)

- [ ] Setup Prometheus + Grafana
- [ ] Add metrics:

  - [ ] Crawl rate (pages/sec)
  - [ ] Error rate (403, 429, 5xx)
  - [ ] Proxy health
  - [ ] Duplicate rate

- [ ] Add alerting (proxy die, error spike)
- [ ] Implement retry + circuit breaker logic
- [ ] Scale test: 2 VPS - 10k page/day

### Phase 4: Production & Expansion (2+ weeks)

- [ ] Build Site Config System (yaml / json)
- [ ] Implement Scheduler (daily/hourly job)
- [ ] Build API (FastAPI / Flask) to serve job data
- [ ] Option: Build mini Web UI
- [ ] Add new sites (VietnamWorks, CareerBuilder...)
- [ ] Scale horizontally (multi-worker, multi-VPS)

---

## Phase 1 Implementation Status ✅

**COMPLETED**: Single-site crawler for ITviec.com

### Project Structure

```
spiderjobs-distributed-system/
├── crawler.py              # Main crawler script
├── parsers/
│   ├── __init__.py         # Parsers module init
│   └── itviec.py           # ITviec parser implementation
├── docs/                   # Documentation
│   ├── README.md           # Documentation overview
│   └── PHASE1_SUMMARY.md   # Phase 1 implementation summary
├── outputs/                # CSV output files
│   └── .gitkeep           # Keep directory in git
├── config.py              # Configuration settings
├── requirements.txt        # Python dependencies
├── test_crawler.py         # Test script
├── demo.py                # Feature demonstration
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Features Implemented

✅ **Fetch HTML pages** - Uses requests with retry strategy and browser-like headers  
✅ **Parse job listings** - Extracts title, link, company, location, posted date, logo, skills  
✅ **Handle pagination** - Crawls multiple pages (configurable)  
✅ **Save to CSV** - Outputs structured data to CSV files  
✅ **Adapter pattern** - Modular parser design for easy extension  
✅ **Error handling** - Robust error handling and logging  
✅ **Politeness** - Configurable delays between requests  
✅ **Command line interface** - Full CLI with arguments

### Quick Start

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the crawler:**

   ```bash
   # Basic usage - crawl 3 pages
   python crawler.py

   # Crawl 5 pages with custom output file
   python crawler.py --pages 5 --output outputs/my_jobs.csv

   # Search for specific jobs (e.g., "python developer")
   python crawler.py --query "python developer" --pages 2

   # Custom delay between requests (be polite!)
   python crawler.py --delay 2.0
   ```

3. **Test the crawler:**

   ```bash
   python test_crawler.py
   ```

### Usage Examples

```bash
# Crawl first 3 pages (default)
python crawler.py

# Crawl 10 pages with search query
python crawler.py --pages 10 --query "react developer"

# Save to custom file with 2-second delay
python crawler.py --pages 5 --output outputs/react_jobs.csv --delay 2.0
```

### Output Format

The crawler saves job data to CSV with the following fields:

- `title` - Job title
- `link` - Full URL to job posting
- `company` - Company name
- `location` - Job location (city/remote/hybrid)
- `posted_date` - When the job was posted
- `logo_url` - Company logo URL
- `skills` - Comma-separated list of technologies/skills

All output files are saved in the `outputs/` directory.

### Next Steps (Phase 2)

- [ ] Setup Redis for URL frontier queue
- [ ] Implement URL producer and consumer workers
- [ ] Add TopDev parser
- [ ] Implement deduplication service
- [ ] Add proxy pool support

---

## Recommended Tech Stack

| Component           | Stack                                 |
| ------------------- | ------------------------------------- |
| Queue / Frontier    | Redis                                 |
| Worker / Downloader | Python Celery + Requests + Playwright |
| Parser              | BeautifulSoup / Playwright            |
| Deduplication       | Redis Set / Bloom Filter              |
| Storage             | MongoDB / ElasticSearch               |
| Monitoring          | Prometheus + Grafana                  |
| Deploy              | Docker Compose                        |

_Project: spiderjobs-distributed-system 🚀_

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

- [ ] Setup Git repo for crawler project
- [ ] Implement single-site crawler (ITviec)

  - [ ] Fetch HTML page
  - [ ] Parse: title, link, company, location, posted date, logo
  - [ ] Save to CSV / MongoDB

- [ ] Handle pagination (crawl multiple pages)
- [ ] Implement adapter pattern for Parser

  - [ ] ITviecParser

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

---

## Notes

- Team: 2 dev (junior + middle) + ChatGPT support
- Cost: \~\$50-70/month infra VPS + proxy
- MVP target: ready in \~6 weeks
- Scale target: 10k-100k pages/day

---

_Project: spiderjobs-distributed-system 🚀_

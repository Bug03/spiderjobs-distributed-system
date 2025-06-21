#!/usr/bin/env python3
"""
SpiderJobs Distributed Crawler - Phase 1: ITviec Crawler
Main crawler script for ITviec.com job listings
"""

import csv
import time
import logging
from typing import List, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from parsers.itviec import ITviecParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class JobListing:
    """Data class for job listing information"""
    title: str
    link: str
    company: str
    location: str
    posted_date: str
    logo_url: str
    skills: List[str] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []


class ITviecCrawler:
    """Main crawler class for ITviec.com"""
    
    def __init__(self, base_url: str = "https://itviec.com", delay: float = 1.0):
        self.base_url = base_url
        self.delay = delay  # Politeness delay between requests
        self.parser = ITviecParser()
        
        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Headers to appear more like a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch HTML content from a URL with error handling"""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def crawl_jobs(self, max_pages: int = 3, query: str = "") -> List[JobListing]:
        """
        Crawl job listings from ITviec
        
        Args:
            max_pages: Maximum number of pages to crawl
            query: Search query (optional)
            
        Returns:
            List of JobListing objects
        """
        all_jobs = []
        base_jobs_url = f"{self.base_url}/it-jobs"
        
        for page_num in range(1, max_pages + 1):
            # Construct URL for current page
            if page_num == 1:
                url = f"{base_jobs_url}?query={query}" if query else base_jobs_url
            else:
                url = f"{base_jobs_url}?page={page_num}&query={query}"
            
            # Fetch page content
            html_content = self.fetch_page(url)
            if not html_content:
                logger.warning(f"Failed to fetch page {page_num}, skipping...")
                continue
            
            # Parse jobs from current page
            try:
                jobs_on_page = self.parser.parse_jobs(html_content, self.base_url)
                all_jobs.extend(jobs_on_page)
                logger.info(f"Page {page_num}: Found {len(jobs_on_page)} jobs")
                
                # If no jobs found, we might have reached the end
                if not jobs_on_page:
                    logger.info(f"No jobs found on page {page_num}, stopping...")
                    break
                    
            except Exception as e:
                logger.error(f"Error parsing page {page_num}: {e}")
                continue
            
            # Politeness delay
            if page_num < max_pages:
                time.sleep(self.delay)
        
        logger.info(f"Total jobs crawled: {len(all_jobs)}")
        return all_jobs
    
    def save_to_csv(self, jobs: List[JobListing], filename: str = "outputs/itviec_jobs.csv"):
        """Save job listings to CSV file"""
        if not jobs:
            logger.warning("No jobs to save")
            return
        
        # Ensure outputs directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['title', 'link', 'company', 'location', 'posted_date', 'logo_url', 'skills']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for job in jobs:
                    job_dict = asdict(job)
                    # Convert skills list to comma-separated string
                    job_dict['skills'] = ', '.join(job.skills) if job.skills else ''
                    writer.writerow(job_dict)
            
            logger.info(f"Saved {len(jobs)} jobs to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def save_to_mongodb(self, jobs: List[JobListing], 
                       connection_string: str = "mongodb://localhost:27017/",
                       database: str = "spiderjobs", 
                       collection: str = "jobs"):
        """
        Save job listings to MongoDB (optional - requires pymongo)
        
        This method is commented out as MongoDB might not be available in all environments.
        Uncomment and install pymongo if you want to use MongoDB storage.
        """
        try:
            # Uncomment the following lines if you have pymongo installed
            # from pymongo import MongoClient
            # 
            # client = MongoClient(connection_string)
            # db = client[database]
            # coll = db[collection]
            # 
            # # Convert jobs to dictionaries
            # job_dicts = [asdict(job) for job in jobs]
            # 
            # # Insert jobs (replace existing based on link as unique identifier)
            # for job_dict in job_dicts:
            #     coll.replace_one(
            #         {"link": job_dict["link"]}, 
            #         job_dict, 
            #         upsert=True
            #     )
            # 
            # logger.info(f"Saved {len(jobs)} jobs to MongoDB: {database}.{collection}")
            
            logger.info("MongoDB storage is commented out. Install pymongo and uncomment the code to use it.")
            
        except Exception as e:
            logger.error(f"Error saving to MongoDB: {e}")


def main():
    """Main function to run the crawler"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ITviec Job Crawler')
    parser.add_argument('--pages', type=int, default=3, help='Number of pages to crawl (default: 3)')
    parser.add_argument('--query', type=str, default='', help='Search query (default: empty)')
    parser.add_argument('--output', type=str, default='outputs/itviec_jobs.csv', help='Output CSV filename (default: outputs/itviec_jobs.csv)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    # Initialize crawler
    crawler = ITviecCrawler(delay=args.delay)
    
    # Crawl jobs
    logger.info(f"Starting ITviec crawler - Pages: {args.pages}, Query: '{args.query}'")
    jobs = crawler.crawl_jobs(max_pages=args.pages, query=args.query)
    
    # Save results
    if jobs:
        crawler.save_to_csv(jobs, args.output)
        logger.info(f"Crawling completed! Found {len(jobs)} jobs.")
        
        # Print sample of results
        logger.info("Sample results:")
        for i, job in enumerate(jobs[:3]):
            logger.info(f"  {i+1}. {job.title} at {job.company} ({job.location})")
    else:
        logger.warning("No jobs found!")


if __name__ == "__main__":
    main()

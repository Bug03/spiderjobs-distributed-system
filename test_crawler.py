#!/usr/bin/env python3
"""
Test script for ITviec crawler
Run this to test the crawler functionality
"""

import sys
import os

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler import ITviecCrawler, JobListing


def test_crawler():
    """Test the crawler with a small number of pages"""
    print("🕷️  Testing ITviec Crawler")
    print("=" * 50)
    
    # Initialize crawler
    crawler = ITviecCrawler(delay=2.0)  # Be polite with 2-second delay
    
    # Test with just 1 page first
    print("🔍 Crawling 1 page from ITviec...")
    jobs = crawler.crawl_jobs(max_pages=1)
    
    if jobs:
        print(f"✅ Successfully found {len(jobs)} jobs!")
        print("\n📋 Sample job listings:")
        print("-" * 30)
        
        for i, job in enumerate(jobs[:5], 1):
            print(f"{i}. {job.title}")
            print(f"   Company: {job.company}")
            print(f"   Location: {job.location}")
            print(f"   Posted: {job.posted_date}")
            if job.skills:
                print(f"   Skills: {', '.join(job.skills[:3])}")
            print(f"   Link: {job.link[:60]}...")
            print()
        
        # Save to CSV
        output_file = "outputs/test_itviec_jobs.csv"
        crawler.save_to_csv(jobs, output_file)
        print(f"💾 Results saved to: {output_file}")
        
    else:
        print("❌ No jobs found. This might indicate:")
        print("   - Network connectivity issues")
        print("   - Website structure changes")
        print("   - Parsing logic needs adjustment")


if __name__ == "__main__":
    test_crawler()

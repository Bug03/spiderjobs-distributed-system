#!/usr/bin/env python3
"""
Demo script showcasing Phase 1 ITviec Crawler capabilities
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler import ITviecCrawler


def demo_basic_crawling():
    """Demo basic crawling functionality"""
    print("🚀 Demo 1: Basic Job Crawling")
    print("=" * 40)
    
    crawler = ITviecCrawler(delay=1.5)
    jobs = crawler.crawl_jobs(max_pages=1)
    
    if jobs:
        print(f"✅ Found {len(jobs)} jobs from 1 page")
        
        # Show sample job
        sample_job = jobs[0]
        print(f"\n📄 Sample Job:")
        print(f"   Title: {sample_job.title}")
        print(f"   Company: {sample_job.company}")
        print(f"   Location: {sample_job.location}")
        print(f"   Posted: {sample_job.posted_date}")
        print(f"   Skills: {', '.join(sample_job.skills[:5])}")
        
        # Save to CSV
        crawler.save_to_csv(jobs, "outputs/demo_basic.csv")
        print(f"   📁 Saved to: outputs/demo_basic.csv")
    else:
        print("❌ No jobs found")
    
    return jobs


def demo_search_query():
    """Demo search functionality"""
    print("\n🔍 Demo 2: Search Query")
    print("=" * 40)
    
    crawler = ITviecCrawler(delay=1.5)
    
    # Search for React jobs
    print("Searching for 'react' jobs...")
    react_jobs = crawler.crawl_jobs(max_pages=1, query="react")
    
    if react_jobs:
        print(f"✅ Found {len(react_jobs)} React-related jobs")
        
        # Filter jobs that actually mention React
        react_filtered = [job for job in react_jobs if 'react' in job.title.lower() or 'react' in job.skills.__str__().lower()]
        print(f"   📊 {len(react_filtered)} jobs specifically mention React")
        
        if react_filtered:
            sample = react_filtered[0]
            print(f"\n📄 Sample React Job:")
            print(f"   Title: {sample.title}")
            print(f"   Company: {sample.company}")
            print(f"   React Skills: {[s for s in sample.skills if 'react' in s.lower()]}")
        
        # Save to CSV
        crawler.save_to_csv(react_jobs, "outputs/demo_react_jobs.csv")
        print(f"   📁 Saved to: outputs/demo_react_jobs.csv")
    
    return react_jobs


def demo_pagination():
    """Demo pagination functionality"""
    print("\n📚 Demo 3: Pagination")
    print("=" * 40)
    
    crawler = ITviecCrawler(delay=1.0)
    
    print("Crawling 2 pages...")
    jobs = crawler.crawl_jobs(max_pages=2)
    
    if jobs:
        print(f"✅ Found {len(jobs)} jobs across 2 pages")
        
        # Show distribution
        unique_companies = set(job.company for job in jobs if job.company != "N/A")
        unique_locations = set(job.location for job in jobs if job.location != "N/A")
        
        print(f"   🏢 {len(unique_companies)} unique companies")
        print(f"   📍 {len(unique_locations)} unique locations")
        print(f"   🏷️  Top locations: {', '.join(list(unique_locations)[:3])}")
        
        # Save to CSV
        crawler.save_to_csv(jobs, "outputs/demo_pagination.csv")
        print(f"   📁 Saved to: outputs/demo_pagination.csv")
    
    return jobs


def demo_data_analysis():
    """Demo basic data analysis"""
    print("\n📊 Demo 4: Data Analysis")
    print("=" * 40)
    
    # Use jobs from pagination demo
    crawler = ITviecCrawler(delay=1.0)
    jobs = crawler.crawl_jobs(max_pages=1)
    
    if jobs:
        # Analyze skills
        all_skills = []
        for job in jobs:
            all_skills.extend(job.skills)
        
        # Count skill frequency
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Top skills
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        print(f"📈 Top Skills (from {len(jobs)} jobs):")
        for i, (skill, count) in enumerate(top_skills, 1):
            print(f"   {i:2d}. {skill}: {count} jobs")
        
        # Location analysis
        location_counts = {}
        for job in jobs:
            if job.location != "N/A":
                location_counts[job.location] = location_counts.get(job.location, 0) + 1
        
        print(f"\n📍 Job Locations:")
        for location, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {location}: {count} jobs")


def main():
    """Run all demos"""
    print("🕷️  ITviec Crawler - Phase 1 Demo")
    print("=" * 50)
    print("This demo showcases all implemented features:")
    print("✅ HTML fetching with error handling")
    print("✅ Job parsing (title, company, location, date, logo, skills)")
    print("✅ Pagination support")
    print("✅ Search queries")
    print("✅ CSV export")
    print("✅ Adapter pattern architecture")
    print("✅ Politeness delays")
    print()
    
    try:
        # Run demos
        demo_basic_crawling()
        time.sleep(2)
        
        demo_search_query()
        time.sleep(2)
        
        demo_pagination()
        time.sleep(2)
        
        demo_data_analysis()
        
        print("\n🎉 Demo completed successfully!")
        print("\nFiles created:")
        print("   - outputs/demo_basic.csv")
        print("   - outputs/demo_react_jobs.csv") 
        print("   - outputs/demo_pagination.csv")
        
        print("\n🚀 Ready for Phase 2: Queue-based Pipeline!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")


if __name__ == "__main__":
    main()

"""
ITviec Parser - Extract job listings from ITviec.com
"""

import re
import logging
from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


class ITviecParser:
    """Parser for ITviec.com job listings"""
    
    def __init__(self):
        self.job_selectors = {
            # Main job container
            'job_container': 'div[data-search-id]',
            # Alternative selector if the above doesn't work
            'job_container_alt': '.job-item, .search-result-item, [class*="job"]',
            # Job title selectors
            'title': 'h3 a, .job-title a, [class*="title"] a',
            'title_alt': 'h3, .job-title, [class*="title"]',
            # Company selectors
            'company': '[class*="company"] a, .company-name a, .employer a',
            'company_alt': '[class*="company"], .company-name, .employer',
            # Location selectors
            'location': '[class*="location"], .job-location, .location',
            # Date selectors
            'date': '[class*="date"], .posted-date, .time, [class*="time"]',
            # Logo selectors
            'logo': 'img[src*="logo"], img[alt*="logo"], .company-logo img, .logo img',
            # Skills selectors
            'skills': '[class*="skill"], .skills a, .tag, [class*="tag"]'
        }
    
    def parse_jobs(self, html_content: str, base_url: str) -> List:
        """
        Parse job listings from ITviec HTML content
        
        Args:
            html_content: Raw HTML content from ITviec
            base_url: Base URL for resolving relative links
            
        Returns:
            List of JobListing objects
        """
        from crawler import JobListing  # Import here to avoid circular import
        
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs = []
        
        # Find job containers using multiple selectors
        job_containers = self._find_job_containers(soup)
        
        if not job_containers:
            logger.warning("No job containers found on page")
            return jobs
        
        logger.info(f"Found {len(job_containers)} job containers")
        
        for container in job_containers:
            try:
                job = self._parse_single_job(container, base_url)
                if job and job.title and job.link:  # Only add if we have essential fields
                    jobs.append(job)
            except Exception as e:
                logger.warning(f"Error parsing job container: {e}")
                continue
        
        return jobs
    
    def _find_job_containers(self, soup: BeautifulSoup) -> List[Tag]:
        """Find job listing containers using multiple selector strategies"""
        
        # Try primary selector
        containers = soup.select(self.job_selectors['job_container'])
        if containers:
            return containers
        
        # Try alternative selectors
        for selector in self.job_selectors['job_container_alt'].split(', '):
            containers = soup.select(selector.strip())
            if containers:
                logger.info(f"Found containers using selector: {selector}")
                return containers
        
        # If specific selectors fail, try to find job patterns by content
        # Look for elements containing job-related keywords
        containers = []
        for element in soup.find_all(['div', 'article', 'section']):
            # Check if element contains job-like content
            text_content = element.get_text().lower()
            if any(keyword in text_content for keyword in ['developer', 'engineer', 'manager', 'analyst', 'designer']):
                # Check if it has a link that looks like a job
                job_link = element.find('a', href=True)
                if job_link and any(pattern in job_link.get('href', '') for pattern in ['/it-jobs/', '/jobs/', 'job']):
                    containers.append(element)
        
        # Remove duplicates and nested containers
        unique_containers = []
        for container in containers:
            is_nested = any(container in parent.descendants for parent in unique_containers)
            if not is_nested:
                unique_containers.append(container)
        
        return unique_containers[:20]  # Limit to reasonable number
    
    def _parse_single_job(self, container: Tag, base_url: str):
        """Parse a single job container into a JobListing object"""
        from crawler import JobListing  # Import here to avoid circular import
        
        # Extract title and link
        title, link = self._extract_title_and_link(container, base_url)
        
        # Extract company
        company = self._extract_company(container)
        
        # Extract location
        location = self._extract_location(container)
        
        # Extract posted date
        posted_date = self._extract_posted_date(container)
        
        # Extract logo URL
        logo_url = self._extract_logo_url(container, base_url)
        
        # Extract skills
        skills = self._extract_skills(container)
        
        return JobListing(
            title=title or "N/A",
            link=link or "",
            company=company or "N/A",
            location=location or "N/A", 
            posted_date=posted_date or "N/A",
            logo_url=logo_url or "",
            skills=skills
        )
    
    def _extract_title_and_link(self, container: Tag, base_url: str):
        """Extract job title and link"""
        title, link = "", ""
        
        # Try title selectors
        for selector in self.job_selectors['title'].split(', '):
            title_element = container.select_one(selector.strip())
            if title_element:
                title = self._clean_text(title_element.get_text())
                link = title_element.get('href', '')
                if link:
                    link = urljoin(base_url, link)
                break
        
        # If no link found in title, try alternative approach
        if not link:
            for selector in self.job_selectors['title_alt'].split(', '):
                title_element = container.select_one(selector.strip())
                if title_element:
                    if not title:
                        title = self._clean_text(title_element.get_text())
                    # Look for nearest link
                    link_element = title_element.find('a') or title_element.find_parent('a') or container.find('a', href=True)
                    if link_element:
                        link = urljoin(base_url, link_element.get('href', ''))
                    break
        
        return title, link
    
    def _extract_company(self, container: Tag):
        """Extract company name"""
        company = ""
        
        # Try specific ITviec patterns first
        company_patterns = [
            'a[href*="/companies/"]',  # ITviec company links
            '[class*="company"] a',
            '.company-name a',
            '.employer a'
        ]
        
        for pattern in company_patterns:
            company_element = container.select_one(pattern)
            if company_element:
                company_text = self._clean_text(company_element.get_text())
                # Filter out very long text and common non-company text
                if company_text and len(company_text) < 100 and not any(word in company_text.lower() 
                    for word in ['view', 'jobs', 'sign in', 'salary', 'image']):
                    company = company_text
                    break
        
        # Try alternative selectors
        if not company:
            for selector in self.job_selectors['company_alt'].split(', '):
                company_element = container.select_one(selector.strip())
                if company_element:
                    company_text = self._clean_text(company_element.get_text())
                    if company_text and len(company_text) < 100:
                        company = company_text
                        break
        
        # If still no company, try to extract from link text patterns
        if not company:
            links = container.find_all('a', href=True)
            for link in links:
                if hasattr(link, 'get'):
                    href = link.get('href', '') or ''
                    if '/companies/' in str(href):
                        company_text = self._clean_text(link.get_text())
                        if company_text and len(company_text) < 100 and not any(word in company_text.lower() 
                            for word in ['view', 'jobs', 'sign in', 'salary', 'image']):
                            company = company_text
                            break
        
        return company
    
    def _extract_location(self, container: Tag):
        """Extract job location"""
        location = ""
        
        for selector in self.job_selectors['location'].split(', '):
            location_element = container.select_one(selector.strip())
            if location_element:
                location = self._clean_text(location_element.get_text())
                # Common location patterns in Vietnam
                if any(city in location.lower() for city in ['ho chi minh', 'ha noi', 'da nang', 'can tho']):
                    break
        
        # If no specific location found, look for text patterns
        if not location:
            text_content = container.get_text()
            location_patterns = [
                r'Ho Chi Minh',
                r'Ha Noi',
                r'Da Nang', 
                r'Can Tho',
                r'Hybrid',
                r'Remote',
                r'At office'
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    location = match.group()
                    break
        
        return location
    
    def _extract_posted_date(self, container: Tag):
        """Extract posted date"""
        posted_date = ""
        
        for selector in self.job_selectors['date'].split(', '):
            date_element = container.select_one(selector.strip())
            if date_element:
                date_text = self._clean_text(date_element.get_text())
                # Look for date patterns
                if any(pattern in date_text.lower() for pattern in ['posted', 'ago', 'hour', 'minute', 'day', 'week']):
                    posted_date = date_text
                    break
        
        # Look for date patterns in the entire container text
        if not posted_date:
            text_content = container.get_text()
            date_patterns = [
                r'Posted \d+ \w+ ago',
                r'\d+ hours? ago',
                r'\d+ minutes? ago', 
                r'\d+ days? ago',
                r'HOT Posted \d+ \w+ ago',
                r'SUPER HOT Posted \d+ \w+ ago'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    posted_date = match.group()
                    break
        
        return posted_date
    
    def _extract_logo_url(self, container: Tag, base_url: str):
        """Extract company logo URL"""
        logo_url = ""
        
        for selector in self.job_selectors['logo'].split(', '):
            logo_element = container.select_one(selector.strip())
            if logo_element and hasattr(logo_element, 'get'):
                src = logo_element.get('src', '')
                if src:
                    logo_url = urljoin(base_url, str(src))
                    break
        
        # Alternative: look for any image that might be a logo
        if not logo_url:
            images = container.find_all('img')
            for img in images:
                if hasattr(img, 'get') and hasattr(img, 'name') and img.name == 'img':
                    src = img.get('src', '')
                    alt = img.get('alt', '') or ''
                    alt_str = str(alt).lower() if alt else ''
                    src_str = str(src).lower() if src else ''
                    
                    if src and ('logo' in src_str or 'logo' in alt_str or 'company' in alt_str):
                        logo_url = urljoin(base_url, str(src))
                        break
        
        return logo_url
    
    def _extract_skills(self, container: Tag):
        """Extract skills/technologies mentioned"""
        skills = []
        
        for selector in self.job_selectors['skills'].split(', '):
            skill_elements = container.select(selector.strip())
            for element in skill_elements:
                skill_text = self._clean_text(element.get_text())
                if skill_text and len(skill_text) < 50:  # Reasonable skill name length
                    skills.append(skill_text)
        
        # Look for common tech skills in text
        if not skills:
            text_content = container.get_text()
            common_skills = [
                'Python', 'Java', 'JavaScript', 'TypeScript', 'ReactJS', 'VueJS', 'Angular',
                'NodeJS', 'PHP', 'C#', 'C++', 'Go', 'Rust', 'Swift', 'Kotlin',
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'MongoDB', 'PostgreSQL',
                'MySQL', 'Redis', 'Git', 'Jenkins', 'CI/CD', 'Agile', 'Scrum'
            ]
            
            for skill in common_skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', text_content, re.IGNORECASE):
                    skills.append(skill)
        
        return list(set(skills))  # Remove duplicates
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common unwanted patterns
        text = re.sub(r'^\s*[\u2022\u2023\u25E6\u2043\u2219]\s*', '', text)  # Remove bullet points
        text = re.sub(r'\s*\[Image:.*?\]\s*', '', text)  # Remove [Image: ...] patterns
        
        return text

# Configuration for ITviec Crawler
# This file contains settings that can be easily modified

# Crawler settings
CRAWLER_CONFIG = {
    "base_url": "https://itviec.com",
    "default_delay": 1.0,  # seconds between requests
    "max_retries": 3,
    "timeout": 10,  # seconds
    "default_pages": 3,
}

# Request headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Output settings
OUTPUT_CONFIG = {
    "default_csv_filename": "outputs/itviec_jobs.csv",
    "csv_encoding": "utf-8",
    "outputs_dir": "outputs/",
}

# MongoDB settings (for future use)
MONGODB_CONFIG = {
    "connection_string": "mongodb://localhost:27017/",
    "database": "spiderjobs",
    "collection": "jobs",
}

# Site-specific configurations (for Phase 2)
SITE_CONFIGS = {
    "itviec": {
        "base_url": "https://itviec.com",
        "jobs_path": "/it-jobs",
        "rate_limit": 1.0,  # seconds between requests
        "parser_class": "ITviecParser",
    },
    # Future sites can be added here
    "topdev": {
        "base_url": "https://topdev.vn", 
        "jobs_path": "/it-jobs",
        "rate_limit": 1.5,
        "parser_class": "TopDevParser",  # To be implemented in Phase 2
    },
    "vietnamworks": {
        "base_url": "https://vietnamworks.com",
        "jobs_path": "/tim-viec-lam",
        "rate_limit": 2.0,
        "parser_class": "VietnamWorksParser",  # To be implemented in Phase 2
    }
}

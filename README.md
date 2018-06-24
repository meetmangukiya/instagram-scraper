# Instagram-Scraper

## Installation

This scraper uses `requests_html` which requires python 3.6 or higher runtime.

```bash
pip install -r requirements.txt
```

## Usage

### As library

```python
from instagram_scraper import scrape_instagram

for url, caption, hashtags, mentions in scrape_instagram(['quotes', 'meet'], 5):
    print(url, caption, hashtags, mentions)
```

### As script

```bash
python3 instagram_scraper.py --tags software bugs --count 50
```

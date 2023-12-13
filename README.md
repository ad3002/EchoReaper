# EchoReaper
A small library for scraping websites using proxy

## Installation
```bash
pip install EchoReaper
```

Or you can install from source:

```
git clone https://github.com/ad3002/EchoReaper.git
cd EchoReaper
python setup.py install
```

## Usage

Simple case of scraping pages without proxy:

```python
from EchoReaper import iter_page_sources

with open("url_to_download.txt") as fh:
    urls = list(set(map(lambda x: x.strip(), fh.readlines())))

for ii, (url, source) in enumerate(iter_page_sources(urls, use_proxy=False, minimum_size=10000, headless=headless, timeout=10, has_token=None)):

    output_file = os.path.join(name, "pages", url.split("/")[-1] + ".html")
    
    with open(output_file, 'w') as file:
        file.write(source)
```

Simple case of scraping pages with proxy:

```python
from EchoReaper import iter_page_sources

with open("url_to_download.txt") as fh:
    urls = list(set(map(lambda x: x.strip(), fh.readlines())))

for ii, (url, source) in enumerate(iter_page_sources(urls, use_proxy=True, minimum_size=10000, headless=headless, timeout=10, has_token=None)):

    output_file = os.path.join(name, "pages", url.split("/")[-1] + ".html")
    
    with open(output_file, 'w') as file:
        file.write(source)
```
# crawler

A web crawler with different strategies

## How to use

To just see what pages are being crawled:

```py
c = Crawler('http://reelradio.com', CrawlerStrategy())
c.crawl()
```

Or to print each page, use the `PrinterStrategy()`

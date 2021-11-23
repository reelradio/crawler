# crawler

A web crawler with different strategies

## How to use

At minimum, supply a `url` and a `CrawlerStrategy` to the constructor, then use `crawl()`:

```py
c = Crawler('http://reelradio.com', CrawlerStrategy())
c.crawl()
```

Configure the crawler by passing more parameters to the constructor:

```py
# crawl yahoo, only taking absolute links, to a max depth of 3
c = Crawler('https://yahoo.com', CrawlerStrategy(), relative_urls=False, max_depth=3)
c.crawl()


# crawl and ignore links starting with #, or ending with pdf/java,
# and indent the output based on recursion depth
c = Crawler('https://zedchance.github.io/notes', CrawlerStrategy(),
            ignore_prefixes=('#',),
            ignore_suffixes=('pdf', 'java'),
            indent_depth=True)

# Print out all text from xkcd, no recursive crawling
c = Crawler('https://xkcd.com', PrinterStrategy(), explore=False)

# or setup a dictionary
config = {
    "explore": True,
    "relative_urls": True,
    "max_depth": 3,
    "ignore_prefixes": ('http', 'mailto', '#'),
    "indent_depth": True,
}
c = Crawler('http://reelradio.com/index.html', CrawlerStrategy(), ** config)
```

### Strategies

The `CrawlerStrategy` interface demands an `execute` functions that processes a [`BeautifulSoup4`](https://www.crummy.com/software/BeautifulSoup/) object.

```py
class MyStrategy(CrawlerStrategy):
    def execute(self, soup):
        # do stuff with soup
```

- `PrinterStrategy` prints out all text from the page.
- `TagStrategy` generates a list of words and occurences

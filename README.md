# crawler

A web crawler with different strategies

## How to use

At minimum, supply a `url` to the constructor, then use `crawl()`:

```py
c = Crawler('https://xkcd.com')
c.crawl()
```

Specify the maximum recursion depth, and only take absolute links:

```py
c = Crawler('https://yahoo.com', relative_urls=False, max_depth=3)
c.crawl()
```

Ignore links starting with or ending with keywords, and indent the output based on recursion depth:

```py
c = Crawler('https://zedchance.github.io/notes',
            ignore_prefixes=('#',),
            ignore_suffixes=('pdf', 'java', 'docx', 'pptx'),
            indent_depth=True)
c.crawl()
```

Note that `ignore_prefixes` and `ignore_suffixes` take tuples of strings as the parameter.

Or build a dictionary:

```py
config = {
    "explore": True,
    "relative_urls": True,
    "max_depth": 3,
    "ignore_prefixes": ('http', 'mailto', '#'),
    "ignore_suffixes": ('docx', ),
    "indent_depth": True,
}
c = Crawler('http://reelradio.com/index.html', **config)
c.crawl()
```

### Strategies

The `CrawlerStrategy` interface demands an `execute` functions that processes a [`BeautifulSoup4`](https://www.crummy.com/software/BeautifulSoup/) object.

```py
class MyStrategy(CrawlerStrategy):
    def execute(self, soup):
        # do stuff with soup
```

- `CrawlerStrategy` is the default strategy if no parameter is passed, this strategy does nothing
- `PrinterStrategy` prints out all text from the page
- `TagStrategy` generates a list of words and occurences

When testing strategies it is convenient to use `explore=False` to only visit the first page.

To print out the page's text:

```py
c = Crawler('https://xkcd.com', strategy=PrinterStrategy(), explore=False)
c.crawl()
```

To see a list of tags:

```py
c = Crawler('https://xkcd.com', strategy=TagStrategy(), explore=False)
c.crawl()
```

# a web page crawler with different strategies
import math

import requests
from bs4 import BeautifulSoup
from requests_toolbelt import sessions


class CrawlerStrategy:
    def execute(self, soup):
        pass


class PrinterStrategy(CrawlerStrategy):
    def execute(self, soup):
        for s in soup.stripped_strings:
            print(">>>", s)


class TagStrategy(CrawlerStrategy):
    def execute(self, soup):
        tags = {}
        for s in soup.stripped_strings:
            for t in s.split():
                if t not in tags:
                    tags[t] = 1
                else:
                    tags[t] += 1
        for k, v in sorted(tags.items()):
            print(f'{v:3}', k)


class Crawler:
    def __init__(self, url, strategy: CrawlerStrategy, **kwargs):
        self.url = url
        if not isinstance(strategy, CrawlerStrategy):
            raise TypeError("strategy must be implementation of CrawlerStrategy")
        self.strategy = strategy
        self.relative_urls = kwargs.get('relative_urls', True)
        self.explore = kwargs.get('explore', True)
        self.depth = 0
        self.max_depth = kwargs.get('max_depth', math.inf)
        self.indent_depth = kwargs.get('indent_depth', False)
        self.ignore_prefixes = kwargs.get('ignore_prefixes', ('mailto',))
        self.ignore_suffixes = kwargs.get('ignore_suffixes', ('pdf',))
        if self.relative_urls:
            self.ignore_prefixes = self.ignore_prefixes + ('http',)

    def crawl(self):
        visited = {}
        if self.relative_urls:
            http = sessions.BaseUrlSession(base_url=self.url)
        else:
            http = requests

        def _crawl(current_url):
            if current_url in visited:
                return

            # visit
            try:
                page = http.get(current_url)
            except Exception as e:
                return
            soup = BeautifulSoup(page.content, 'html.parser')
            visited[current_url] = page.status_code

            # perform strategy
            if page.status_code == 200:
                print(" " * self.depth if self.indent_depth else "", self.depth, visited[current_url], current_url)
                self.strategy.execute(soup)
            else:
                return

            # explore
            if not self.explore:
                return
            for anchor in soup.find_all('a'):
                if anchor is None or anchor in visited:
                    continue
                next_url = anchor.get('href')
                if next_url is None or next_url.startswith(self.ignore_prefixes) or next_url.endswith(self.ignore_suffixes):
                    continue
                if not next_url.startswith('/') and self.relative_urls:
                    next_url = '/' + next_url

                if self.depth < self.max_depth:
                    self.depth += 1
                    _crawl(next_url)
                    self.depth -= 1
                else:
                    break

        # crawl the site
        _crawl(self.url)


if __name__ == '__main__':
    # c = Crawler('https://yahoo.com', CrawlerStrategy(), relative_urls=False)
    c = Crawler('http://reelradio.com', CrawlerStrategy())
    c.crawl()

# a web page crawler with different strategies

import requests
from bs4 import BeautifulSoup
from requests_toolbelt import sessions


class CrawlerStrategy:
    def execute(self, soup):
        pass


class PrinterStrategy(CrawlerStrategy):
    def execute(self, soup):
        for s in soup.stripped_strings:
            print(s)


class Crawler:
    def __init__(self, url, strategy, relative_urls=True, explore=True):
        self.url = url
        if not isinstance(strategy, CrawlerStrategy):
            raise TypeError("strategy must be implementation of CrawlerStrategy")
        self.strategy = strategy
        self.relative_urls = relative_urls
        self.explore = explore

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
            print(visited[current_url], current_url)

            # perform strategy
            if page.status_code == 200:
                self.strategy.execute(soup)
            else:
                return

            # explore
            if not self.explore:
                return
            for anchor in soup.find_all('a'):
                if anchor is None:
                    continue
                next_url = anchor.get('href')
                if next_url is None:
                    continue
                if not next_url.startswith('/') and self.relative_urls:
                    next_url = '/' + next_url

                _crawl(next_url)

        # crawl the site
        _crawl(self.url)


if __name__ == '__main__':
    # c = Crawler('https://yahoo.com', CrawlerStrategy(), relative_urls=False)
    c = Crawler('http://reelradio.com', CrawlerStrategy())
    c.crawl()

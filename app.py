import logging
from requests import (
    get,
    Response
)
from requests.exceptions import (
    HTTPError,
    RequestException
)
from bs4 import (
    BeautifulSoup,
    Tag
)

URL = 'https://news.ycombinator.com/'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_web_page(url: str) -> Response:
    response = get(url)
    response.raise_for_status()
    return response


class YCombinatorPage:

    def __init__(self, url: str):
        self.parsed = BeautifulSoup(
                get_web_page(
                    url
                    ).text,
                features="html.parser"
                )

    def _get_title(self, tr: Tag) -> str:
        span = tr.find_all('span', attrs={'class': 'titleline'}).pop()
        return span.a.string

    @property
    def news(self) -> list[str]:
        trs = self.parsed.find_all('tr', attrs={'class': 'athing'})
        return [ self._get_title(tr) for tr in trs ]

def main(url: str = URL):
    page = YCombinatorPage(url)
    logger.info(f"Number of news: {len(page.news)}")
    logger.info("News:")
    for i, new in enumerate(page.news):
        logger.info(f"[{i+1}]: {new}")

if __name__ == "__main__":
    main()

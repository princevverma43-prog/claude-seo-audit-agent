import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import json
import sys


HEADERS = {
    "User-Agent": "Mozilla/5.0 SEO-Audit-Agent/1.0"
}


def normalize_url(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url.rstrip("/")


def crawl_site(start_url, max_pages=50):

    start_url = normalize_url(start_url)

    domain = urlparse(start_url).netloc

    queue = deque([start_url])

    visited = set()

    pages = []

    session = requests.Session()

    session.headers.update(HEADERS)

    while queue and len(visited) < max_pages:

        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        try:

            response = session.get(
                url,
                timeout=15,
                allow_redirects=True
            )

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            title = ""

            if soup.title:

                title = soup.title.get_text(
                    strip=True
                )

            meta_description = ""

            meta = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            if meta:

                meta_description = meta.get(
                    "content",
                    ""
                )

            h1s = [

                h.get_text(
                    " ",
                    strip=True
                )

                for h in soup.find_all("h1")

            ]

            canonical = ""

            canonical_tag = soup.find(
                "link",
                rel="canonical"
            )

            if canonical_tag:

                canonical = canonical_tag.get(
                    "href",
                    ""
                )

            links = []

            for link in soup.find_all(
                "a",
                href=True
            ):

                absolute_url = urljoin(
                    url,
                    link["href"]
                )

                parsed = urlparse(
                    absolute_url
                )

                if parsed.netloc == domain:

                    clean_url = (
                        absolute_url
                        .split("#")[0]
                    )

                    links.append(
                        clean_url
                    )

                    if clean_url not in visited:

                        queue.append(
                            clean_url
                        )

            images = soup.find_all("img")

            missing_alt = sum(

                1

                for image in images

                if not image.get("alt")

            )

            pages.append({

                "url": url,

                "final_url": response.url,

                "status_code":
                    response.status_code,

                "title": title,

                "title_length":
                    len(title),

                "meta_description":
                    meta_description,

                "meta_description_length":
                    len(meta_description),

                "h1s": h1s,

                "h1_count":
                    len(h1s),

                "canonical":
                    canonical,

                "internal_links":
                    links,

                "internal_link_count":
                    len(links),

                "image_count":
                    len(images),

                "images_missing_alt":
                    missing_alt

            })

            print(
                f"Crawled: {url}"
            )

        except Exception as error:

            print(
                f"Error: {url} - {error}"
            )

    return pages


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage: python crawler.py https://example.com"
        )

        sys.exit(1)

    website = sys.argv[1]

    data = crawl_site(
        website,
        max_pages=50
    )

    with open(
        "data/crawl.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\nCrawl complete: {len(data)} pages"
    )

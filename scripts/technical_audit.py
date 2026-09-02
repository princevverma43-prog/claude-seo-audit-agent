import json
from collections import defaultdict


def audit():

    with open(
        "data/crawl.json",
        encoding="utf-8"
    ) as file:

        pages = json.load(file)

    issues = []

    title_map = defaultdict(list)

    for page in pages:

        url = page["url"]

        title = page["title"].strip()

        if title:

            title_map[title].append(url)

        if page["status_code"] != 200:

            issues.append({

                "type": "HTTP Status",

                "url": url,

                "priority": "P0",

                "issue":
                    f"Page returned HTTP {page['status_code']}"

            })

        if not page["canonical"]:

            issues.append({

                "type": "Canonical",

                "url": url,

                "priority": "P1",

                "issue":
                    "Missing canonical tag"

            })

        if page["h1_count"] == 0:

            issues.append({

                "type": "H1",

                "url": url,

                "priority": "P1",

                "issue":
                    "Missing H1"

            })

        if page["images_missing_alt"] > 0:

            issues.append({

                "type": "Images",

                "url": url,

                "priority": "P2",

                "issue":
                    f"{page['images_missing_alt']} images missing alt text"

            })

    for title, urls in title_map.items():

        if len(urls) > 1:

            issues.append({

                "type": "Duplicate Title",

                "title": title,

                "urls": urls,

                "priority": "P1",

                "issue":
                    "Multiple pages use the same title"

            })

    with open(
        "data/technical_issues.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            issues,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Technical audit complete: {len(issues)} issues"
    )


if __name__ == "__main__":

    audit()

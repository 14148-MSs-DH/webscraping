import time
from urllib.parse import urljoin, parse_qs, urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup

START_URL = "https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0167%3Abook%3D1%3Asection%3D327a"
BASE_URL = "https://www.perseus.tufts.edu/hopper/"


def get_soup(url):
    """
    Download one page and turn it into a BeautifulSoup object.
    """
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def extract_greek_text(soup):
    """
    Find the Greek text container and return it as plain text.
    """
    container = soup.select_one("div.text_container.greek")
    if container is None:
        return ""

    # get_text() removes tags. separator=" " keeps words from gluing together.
    text = container.get_text(separator=" ", strip=True)

    # Optional cleanup: collapse repeated whitespace
    text = " ".join(text.split())
    return text


def find_next_url(soup, current_url):
    """
    Find the 'next' link and return an absolute URL, or None if not found.
    """
    # On these pages, the next arrow link is something like: <a class="arrow" href="text?doc=...">
    next_link = soup.select_one('a.arrow img[alt="next"]')
    if next_link is None:
        return None

    # next_link is the <img>, so we go up to its parent <a>
    a_tag = next_link.parent
    href = a_tag.get("href")
    if not href:
        return None

    return urljoin(current_url, href)


def doc_still_in_book1(url):
    """
    Decide whether a URL is still inside book=1.
    Perseus stores these inside the 'doc' query parameter.
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    doc_value_list = query.get("doc", [])
    if not doc_value_list:
        return False

    # e.g. "Republic:text:1999.01.0125:book=1:section=327a"
    doc_value = doc_value_list[0]

    return ":book=1:" in doc_value


def scrape_book1(start_url):
    """
    Follow 'next' links, collect Greek text, stop when leaving book 1 chapter 1.
    """
    url = start_url
    all_sections = []

    with open("Republic_chapter_1.txt", "w", encoding="utf-8") as f:
        section_count = 0

        while True:
            soup = get_soup(url)

            greek = extract_greek_text(soup)
            if greek:
                all_sections.append(greek)
                section_count += 1
                f.write(f"[Section {section_count}]\n")
                f.write(greek)
                f.write("\n\n")
                f.flush()  # 关键：立刻写到磁盘

            next_url = find_next_url(soup, url)
            if next_url is None:
                break

            # Stop once the next URL is no longer chapter 1
            if not doc_still_in_book1(next_url):
                break

            url = next_url

            # Be polite to the server
            time.sleep(0.5)
        print(f"Saved {section_count} sections")

    return all_sections


if __name__ == "__main__":
    sections = scrape_book1(START_URL)
    print(f"Saved {len(sections)} sections to Republic_chapter_1.txt")

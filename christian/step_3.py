import time
from urllib.parse import urljoin, parse_qs, urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup

START_URL = "https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3atext%3a1999.01.0125%3Abook%3D1%3Achapter%3D1%3Asection%3D0"
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


def doc_still_in_book1_chapter1(url):
    """
    Decide whether a URL is still inside book=1 and chapter=1.
    Perseus stores these inside the 'doc' query parameter.
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    doc_value_list = query.get("doc", [])
    if not doc_value_list:
        return False

    doc_value = doc_value_list[0]  # e.g. "Perseus:text:1999.01.0125:book=1:chapter=1:section=3"

    return (":book=1:" in doc_value) and (":chapter=1:" in doc_value)


def scrape_book1_chapter1(start_url):
    """
    Follow 'next' links, collect Greek text, stop when leaving book 1 chapter 1.
    """
    url = start_url
    all_sections = []

    while True:
        soup = get_soup(url)

        greek = extract_greek_text(soup)
        if greek:
            all_sections.append(greek)

        next_url = find_next_url(soup, url)
        if next_url is None:
            break

        # Stop once the next URL is no longer chapter 1
        if not doc_still_in_book1_chapter1(next_url):
            break

        url = next_url

        # Be polite to the server
        time.sleep(0.5)

    return all_sections


if __name__ == "__main__":
    sections = scrape_book1_chapter1(START_URL)

    with open("herodotus_chapter_1.txt", "w", encoding="utf-8") as f:
        for i, section_text in enumerate(sections, start=1):
            # Write each section to a single text file
            f.write(f"[Section {i}]\n")
            f.write(section_text)
            f.write("\n\n")

            # Also print to console
            print(f"[Section {i}]")
            print(section_text)
            print()

    print(f"Saved {len(sections)} sections to herodotus_chapter_1.txt")

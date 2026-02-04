import time
from urllib.parse import urljoin, parse_qs, urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup

TEXT_ID = "1999.01.0126"     
BOOK = "1"
CHAPTER = "1"

START_URL = f"https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3atext%3a{TEXT_ID}%3Abook%3D{BOOK}%3Achapter%3D{CHAPTER}%3Asection%3D0"
OUTPUT_FILE = f"perseus_{TEXT_ID}_book{BOOK}_chapter{CHAPTER}.txt"

def get_soup(url):
    """Download one page and return BeautifulSoup."""
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")

def extract_text(soup):
    """
    Extract main text from Perseus page (English, Greek, Latin).
    """
    
    container = soup.select_one("div.text_container.greek")

    if container is None:
        container = soup.select_one("div.text_container")

    if container is None:
        return ""

    text = container.get_text(separator=" ", strip=True)
    return " ".join(text.split())

def find_next_url(soup, current_url):
    """
    Find the 'next section' arrow link.
    """
    next_link = soup.select_one('a.arrow img[alt="next"]')
    if next_link is None:
        return None

    a_tag = next_link.parent
    href = a_tag.get("href")
    if not href:
        return None

    return urljoin(current_url, href)

def still_in_target_section(url):
    """
    Make sure we stay inside the same text, book, and chapter.
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    doc_value_list = query.get("doc", [])
    if not doc_value_list:
        return False

    doc_value = doc_value_list[0]

    return (
        f"Perseus:text:{TEXT_ID}" in doc_value and
        f":book={BOOK}:" in doc_value and
        f":chapter={CHAPTER}:" in doc_value
    )

def scrape_book_chapter(start_url):
    url = start_url
    all_sections = []

    while True:
        soup = get_soup(url)

        text = extract_text(soup)
        if text:
            all_sections.append(text)

        next_url = find_next_url(soup, url)
        if next_url is None or not still_in_target_section(next_url):
            break

        url = next_url
        time.sleep(0.5)  

    return all_sections

if __name__ == "__main__":
    sections = scrape_book_chapter(START_URL)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, section_text in enumerate(sections, start=1):
            f.write(f"[Section {i}]\n")
            f.write(section_text)
            f.write("\n\n")

            print(f"[Section {i}]")
            print(section_text)
            print()

    print(f"Saved {len(sections)} sections to {OUTPUT_FILE}")

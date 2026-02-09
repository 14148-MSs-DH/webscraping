from urllib.request import urlopen
import re

url = "https://www.qalamos.net/receive/MyMssPerson_agent_00001577"
page = urlopen(url)
html = page.read().decode("utf-8")

BASE = "https://www.qalamos.net"

# Regex for manuscript links
pattern = re.compile(
    r'<a href="(.*?)" class="link-manuscript[^"]*">\s*'
    r'\[(.*?)\]\s*'          # Library
    r'([^:]+):\s*'           # Code
    r'(.*?)\s*'              # Title + (Author)
    r'\(([^()]+)\)\s*'       # Author (last parentheses)
    r'</a>',
    re.DOTALL
)

results = []

matches = pattern.findall(html)

for link, library, code, title, author in matches:
    link = BASE + link.strip()
    library = library.strip()
    code = code.strip()
    title = re.sub(r'\s*\([^()]+\)\s*$', '', title.strip())  # remove trailing extra (..)
    author = author.strip()

    results.append((author, title, code, library, link))

# Print results
for author, title, code, library, link in results:
    print(f"Author: {author}")
    print(f"Title: {title}")
    print(f"Code: {code}")
    print(f"Library: {library}")
    print(f"Link: {link}\n")

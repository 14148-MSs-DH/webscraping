# Load the HTML content of a webpage using urllib

from urllib.request import urlopen
url = "https://www.perseus.tufts.edu/hopper/collection?collection=Perseus:collection:Greco-Roman"
page = urlopen(url)
html = page.read().decode("utf-8")
print(html)

# quit()  # Stop execution here for now

# Base for constructing full URLs
BASE = "https://www.perseus.tufts.edu/hopper/"

# Define a regex pattern
import re
pattern = re.compile(r"<td class=\'tdAuthor\'.*?>\s*(.*?)\s*"
                     r"<a href=\"(.*?)\" class=\"aResultsHeader\".*?>\s*(.*?)\s*</a>",
                     re.DOTALL)

# Match and extract data
results = []

matches = pattern.findall(html)
# print(matches)
# quit()

# Loop through results and collect them
for author, link, title in matches:
    # Clean up whitespace
    author = author.strip()
    title = title.strip()
    link = BASE + link.strip()

    # Store the extracted data in the results list
    results.append((author, title, link))

# Print the results
for author, title, link in results:
    print(f"Author: {author}\nTitle: {title}\nLink: {link}\n")
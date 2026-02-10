# Load the HTML content of a webpage using urllib

from urllib.request import urlopen
url = "https://www.dalailalkhayrat.com/parts.php?part=1"
page = urlopen(url)
html = page.read().decode("utf-8")
# print(html)

# quit()  # Stop execution here for now

# Base for constructing full URLs
BASE = "https://www.dalailalkhayrat.com/"

# Define a regex pattern
import re
pattern = re.compile(
    r'<p class="numbers">\s*(\d+).*?</p>'                       
    r'.*?'
    r'<p class="lang arabicText".*?>\s*(.*?)\s*</p>'            
    r'.*?'
    r'<p class="lang translit".*?>\s*(.*?)\s*</p>'              
    r'.*?'
    r'<p class="lang trans".*?lang="en".*?>\s*(.*?)\s*</p>',    
    re.DOTALL
)

# Match and extract data
results = []

matches = pattern.findall(html)

results = []

for number, arabic, translit, english in matches:
    number = number.strip()
    arabic = arabic.strip()
    translit = translit.strip()
    english = english.strip()

    results.append((number, arabic, translit, english))

for number, arabic, translit, english in results:
    print(f"Number: {number}")
    print(f"Arabic: {arabic}")
    print(f"Transliteration: {translit}")
    print(f"English: {english}")
    print("-" * 40)
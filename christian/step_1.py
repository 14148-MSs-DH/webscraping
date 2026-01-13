# We import a single function from Python’s standard library.
# urllib is a built-in module, so we do NOT need to install anything.
# urlopen is the function that opens a web page given a URL.

from urllib.request import urlopen


# This is the address of the web page we want to fetch.
# It is just a normal URL, the same one you could open in a browser.

url = "https://github.com/14148-MSs-DH/webscraping#"


# Here we open the web page.
# Python sends an HTTP request to the server.
# The server responds with the raw contents of the page.
# The result is stored in the variable "page".

page = urlopen(url)


# page.read() reads the raw data returned by the server.
# The data comes in as bytes, not text.
# decode("utf-8") converts those bytes into a normal Python string.
# Finally, we print the HTML source code of the page to the screen.

print(page.read().decode("utf-8"))
# When you run this code, you should see the HTML source code of the page.


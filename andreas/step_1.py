from urllib.request import urlopen

url = "https://www.qalamos.net/receive/MyMssPerson_agent_00001577"

page = urlopen(url)

print(page.read().decode("utf-8"))


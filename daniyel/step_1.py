from urllib.request import urlopen

url = "https://www.syriacheritageproject.org/home?gad_source=1&gad_campaignid=23018615886&gbraid=0AAAABADAZIze9btiYXggd87psNrEKI0Xh&gclid=CjwKCAiA4KfLBhB0EiwAUY7GAY1mA9kV-rUE80C-1h0HBPUQNlevuR0e5Y39EmYvcjxfgm0hQ2O8pxoCLkcQAvD_BwE/"
#url = "https://www.example.com"

print(url)

page = urlopen(url)

print(page.read().decode("utf-8"))
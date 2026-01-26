# 第一步先从目录页面获取所有章节的链接 https://www.wisdomlib.org/hinduism/book/brihat-samhita-sanskrit
# 第二步再从每个文章页面链接里获取每章节内容

from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import time

url = "https://www.wisdomlib.org/hinduism/book/brihat-samhita-sanskrit"

# 这里的page是随机起的变量名，后面可以加.read()等功能是因为内容归于urlopen这个函数返回的HTTPResponse对象的类定义了这些方法

page = urlopen(url)

# page.read()读取服务器返回的原始数据，这些数据是以字节形式返回的，而不是文本形式
# decode("UTF-8")将这些字节转换为普通的Python字符串

html = page.read().decode("UTF-8")

BASE = "https://www.wisdomlib.org/"

# print(html)

# 下面第一步的正则需要的是content界面的title，description，contents部分的标题+chapter name及url

pattern = re.compile(r"<title>(.*?)\s*\[sanskrit\]</title>", re.DOTALL)
matches_title = pattern.search(html)
book_title = matches_title.group(1).strip()

pattern = re.compile(r"<p><em>Summary</em>:\s(.*?)</p>", re.DOTALL)
matches_description = pattern.search(html)
description = matches_description.group(1).strip()

pattern = re.compile(
    r"<a href=\"/(hinduism/book/brihat-samhita-sanskrit/d/[^\"]+)\">\s*(Chapter\s+\d+[^<]+)</a>", re.DOTALL)
matches = pattern.findall(html)

# print(matches)

# 方括号创建一个空的列表用来存储搜索结果，目的和好处是把所有结果集中存储在一个地方，方便后续处理和输出
# 完整逻辑：方括号代表空容器- for loop遍历每个匹配项（注意这里只是遍历而不保存）-把处理后的结果append到列表里（这步才是真正保存结果到容器以便接下来复用或者自定义输出）
search_results = []

# 必须分两步指定括号对应的变量名再=strip是因为findall返回的matches是一个元组列表，必须先拆开元组才能对每个元素进行strip操作（这些str字符串int float等基本数据类型是不可变的immutable，不能直接对元组内的元素进行修改；而像list dict set等装一堆东西的容器才是可变的）
# 三种括号在python里的区别：方括号[]表示列表list或创建一个list对象，小括号()表示元组tuple或调用函数/方法，大括号{}表示字典dict/集合set或创建一个dict/set对象
# for循环直接对应findall返回的每个元组，元组内的每个元素依次赋值给link和chapter_name变量
for chapter_link, chapter_name in matches:
    chapter_link = BASE+chapter_link.strip()
    chapter_name = chapter_name.strip()
    if chapter_name.startswith("Chapter"):
        chapter_name = chapter_name.replace(
            " - ", ": ", 1)  # 把第一个" - "替换成": "，后面的不变以防误伤

    # append防止for循环覆盖前面的结果，每次添加一个新的三元组进去；append后面的圆括号表示调用
    # list.append() 只能接收 1 个参数所以要把多个值放在一个括号里形成一个元组再append
    search_results.append(
        (book_title, description, chapter_link, chapter_name))

# 先只打印一次书名和简介
with open("brihat_samhita_index_sa.txt", "w", encoding="utf-8") as f_index:
    # 书名和简介只写一次
    print(f"Title: {book_title}\n", file=f_index)
    print(f"Description: {description}\n", file=f_index)

    for _, _, chapter_link, chapter_name in search_results:
        print(f"{chapter_name}", file=f_index)
        print(f"Link: {chapter_link}\n", file=f_index)

# 第二步：再从每个文章页面链接里获取每章节内容
with open("brihat_samhita_output_sa.txt", "w", encoding="utf-8") as f_text:
    for _, _, chapter_link, chapter_name in search_results:
        page = urlopen(chapter_link)
        html = page.read().decode("UTF-8")

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(html, 'html.parser')

        content_div = soup.find('div', class_='chapter-content')

        # 删除所有“Analyze grammar / English text”UI块
        for ui in content_div.find_all("span", class_="sanskrit-av"):
            ui.decompose()

        if not content_div:
            print(f"Content not found for {chapter_name}\n")
            continue

        raw_text = content_div.get_text(separator="\n")
        lines = [line.strip() for line in raw_text.split("\n")]
        lines = [line for line in lines if line]

        verses = []
        current = ""

        for line in lines:
            if line.startswith("||"):
                current += " " + line
                verses.append(current.strip())
                current = ""
            elif line == "|":
                current += " |"
            else:
                if current:
                    current += " " + line
                else:
                    current = line

        if current:
            verses.append(current.strip())

        print(f"{chapter_name}\n", file=f_text)
        for v in verses:
            print(v, file=f_text)
        print("", file=f_text)  # 章节间空行
        time.sleep(0.8)
        # quit()  # 先只处理一个章节看看效果

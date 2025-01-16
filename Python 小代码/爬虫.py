import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# 设置目标 URL 和请求头
base_url = "https://news.ycombinator.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# 存储数据
titles = []
links = []

# 爬取内容
for page in range(1, 4):  # 抓取前三页
    url = f"{base_url}?p={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    for item in soup.find_all("a", class_="titlelink"):
        titles.append(item.text)
        links.append(item["href"])

    print(f"完成第 {page} 页爬取")
    time.sleep(random.uniform(1, 3))  # 随机延迟

# 保存数据到 CSV
data = {"Title": titles, "Link": links}
df = pd.DataFrame(data)
df.to_csv("news.csv", index=False, encoding="utf-8-sig")
print("数据已保存到 news.csv")

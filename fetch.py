import urllib.request
import xml.etree.ElementTree as ET
import json
import re

url = 'https://learningenglish.voanews.com/api/z-m_qvy5-it'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

articles = []

try:
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req, timeout=10).read()
    root = ET.fromstring(html)
    
    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else ''
        desc = item.find('description').text if item.find('description') is not None else ''
        clean_desc = re.sub('<[^<]+?>', '', desc).strip()
        if title and clean_desc:
            articles.append({'title': title, 'content': clean_desc})
except Exception as e:
    print(f"Error occurred: {e}")

# 파싱에 실패하거나 비어있어도 최소한의 샘플 데이터를 넣어 파일이 반드시 생성되도록 보장
if not articles:
    articles = [{
        "title": "[VOA] Welcome to VOA English Learner",
        "content": "This is a daily news sample. Select a news story from the menu above to start learning English vocabulary easily."
    }]

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(articles[:10], f, ensure_ascii=False, indent=2)

print("news.json file successfully created.")

import urllib.request
import xml.etree.ElementTree as ET
import json
import re

# 여러 VOA 카테고리 RSS 주소 순회
urls = [
    'https://learningenglish.voanews.com/api/z-$m_qvy5-it',
    'https://learningenglish.voanews.com/api/zone279'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
articles = []

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read()
        root = ET.fromstring(html)
        
        # item 또는 entry 태그 검색
        items = root.findall('.//item')
        for item in items:
            title = item.find('title').text if item.find('title') is not None else ''
            desc = item.find('description').text if item.find('description') is not None else ''
            clean_desc = re.sub('<[^<]+?>', '', desc).strip()
            
            if title and clean_desc and not any(a['title'] == title for a in articles):
                articles.append({'title': title, 'content': clean_desc})
    except Exception as e:
        print(f"URL 요청 실패 ({url}): {e}")

# 파싱 결과가 적을 때를 대비한 기본 샘플 추가
if len(articles) < 3:
    articles.extend([
        {"title": "[VOA Sample 1] Technology Trends in Education", "content": "Technology is changing how students learn around the world. Online tools make it easy to practice languages."},
        {"title": "[VOA Sample 2] Health and Lifestyle Today", "content": "Drinking enough water and getting daily exercise are simple habits that improve focus and overall health."}
    ])

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(articles[:15], f, ensure_ascii=False, indent=2)

print(f"Total {len(articles[:15])} articles saved to news.json")

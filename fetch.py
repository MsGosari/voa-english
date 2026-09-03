import urllib.request
import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime

# VOA 및 NPR 미국 영어 뉴스 RSS 
urls = [
    'https://feeds.npr.org/1001/rss.xml',
    'https://learningenglish.voanews.com/api/z-$m_qvy5-it'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
articles = []

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read()
        root = ET.fromstring(html)
        
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ''
            desc = item.find('description').text if item.find('description') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            
            clean_desc = re.sub('<[^<]+?>', '', desc).strip()
            
            # 날짜 포맷 변환 (YYYY-MM-DD)
            formatted_date = datetime.now().strftime('%Y-%m-%d')
            if pub_date:
                try:
                    # RFC 822 날짜 포맷 파싱
                    dt = datetime.strptime(pub_date[:25].strip(), '%a, %d %b %Y %H:%M:%S')
                    formatted_date = dt.strftime('%Y-%m-%d')
                except:
                    pass

            if title and clean_desc and not any(a['title'] == title for a in articles):
                articles.append({
                    'title': title,
                    'content': clean_desc,
                    'date': formatted_date
                })
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# 정렬: 최신 날짜순
articles.sort(key=lambda x: x['date'], reverse=True)

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(articles[:30], f, ensure_ascii=False, indent=2)

print(f"Saved {len(articles[:30])} articles with date info.")

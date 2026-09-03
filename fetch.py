import urllib.request
import xml.etree.ElementTree as ET
import json
import re

url = 'https://learningenglish.voanews.com/api/z-m_qvy5-it'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    html = urllib.request.urlopen(req).read()
    root = ET.fromstring(html)
    articles = []
    
    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else ''
        desc = item.find('description').text if item.find('description') is not None else ''
        clean_desc = re.sub('<[^<]+?>', '', desc).strip()
        if title and clean_desc:
            articles.append({'title': title, 'content': clean_desc})
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(articles[:10], f, ensure_ascii=False, indent=2)
    print("Successfully created news.json")

except Exception as e:
    print(f"Error fetching RSS: {e}")

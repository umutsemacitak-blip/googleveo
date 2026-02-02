import json
import math
import os
import urllib.parse
from datetime import datetime

BASE_URL = "https://bq5m.com"
ITEMS_PER_PAGE = 30
STATIC_PAGES = [
    "index.html",
    "report-authority-blueprint.html",
    "report-veo-tech.html",
    "report-prompt-research.html",
    "tool-prompt-library.html"
]

def generate_sitemap():
    # Load data.js
    file_path = "data.js"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Strip variable declaration to get JSON content
    # Assuming 'const promptData = { ... }' or similar
    if "const promptData =" in content:
        json_str = content.split("const promptData =")[1].strip()
    else:
        # Fallback if declaration is different
        json_str = content.strip()
    
    if json_str.endswith(";"):
        json_str = json_str[:-1]
    
    try:
        # Replace single quotes with double quotes if necessary?
        # data.js in view looked like valid JSON (double quotes). 
        # But if keys are unquoted this will fail. Let's assume valid JSON syntax for now.
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing data.js: {e}")
        # Attempt to handle JS object literal looser syntax if strictly necessary,
        # but for now let's hope it's clean.
        return

    urls = []
    
    # Static pages
    for page in STATIC_PAGES:
        urls.append({
            "loc": f"{BASE_URL}/{page}",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "daily",
            "priority": "1.0" if page == "index.html" else "0.9"
        })

    # Dynamic Pages (Category and Pagination)
    # Total items for 'All'
    all_prompts_count = sum(len(prompts) for prompts in data.values())
    all_pages = math.ceil(all_prompts_count / ITEMS_PER_PAGE)
    
    # Add 'All' pages
    for p in range(1, all_pages + 1):
        urls.append({
            "loc": f"{BASE_URL}/tool-prompt-library.html?category=All&page={p}",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "weekly",
            "priority": "0.8"
        })

    # Add Category pages
    for category, prompts in data.items():
        cat_encoded = urllib.parse.quote(category)
        
        pages = math.ceil(len(prompts) / ITEMS_PER_PAGE)
        if pages == 0: pages = 1 # Show at least one page even if empty?
        
        for p in range(1, pages + 1):
            urls.append({
                "loc": f"{BASE_URL}/tool-prompt-library.html?category={cat_encoded}&page={p}",
                "lastmod": datetime.now().strftime("%Y-%m-%d"),
                "changefreq": "weekly",
                "priority": "0.7"
            })

    # Generate XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for entry in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{entry["loc"].replace("&", "&amp;")}</loc>\n'
        xml_content += f'    <lastmod>{entry["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{entry["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{entry["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    print(f"Generated sitemap.xml with {len(urls)} URLs.")

if __name__ == "__main__":
    generate_sitemap()

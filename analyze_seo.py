import os
import re
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

FILES_TO_ANALYZE = [
    "index.html",
    "report-authority-blueprint.html",
    "report-veo-tech.html",
    "report-prompt-research.html",
    "tool-prompt-library.html"
]

class SEOReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.in_title = False
        self.meta_description = None
        self.viewport = None
        self.h1_count = 0
        self.headers = [] # list of (level, text)
        self.images_without_alt = 0
        self.total_images = 0
        self.semantic_tags = {tag: 0 for tag in ['header', 'main', 'footer', 'nav', 'article', 'section']}
        self.links = []
        self.structure_stack = []
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == "title":
            self.in_title = True
        
        if tag == "meta":
            name = attrs_dict.get("name", "").lower()
            if name == "description":
                self.meta_description = attrs_dict.get("content", "")
            if name == "viewport":
                self.viewport = attrs_dict.get("content", "")
        
        if tag == "link" and attrs_dict.get("rel") == "canonical":
            self.canonical = attrs_dict.get("href")

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.structure_stack.append(tag)
            if tag == 'h1':
                self.h1_count += 1
        
        if tag == 'img':
            self.total_images += 1
            if not attrs_dict.get('alt'):
                self.images_without_alt += 1
        
        if tag in self.semantic_tags:
            self.semantic_tags[tag] += 1
            
        if tag == 'a':
            href = attrs_dict.get('href')
            if href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if self.structure_stack and self.structure_stack[-1] == tag:
                 # In a real DOM parser we'd grab text here, but stream parsing is tricky for text accumulation across nested tags
                 pass

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
        if self.structure_stack and self.structure_stack[-1] in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.headers.append((self.structure_stack[-1], data.strip()))
            self.structure_stack.pop() # Simplified handling

def analyze_file(filepath):
    if not os.path.exists(filepath):
        return f"FILE NOT FOUND: {filepath}\n"

    parser = SEOReportParser()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            parser.feed(content)
    except Exception as e:
        return f"Error parsing {filepath}: {e}\n"

    report = []
    report.append(f"--- CANALYSIS: {filepath} ---")
    
    # Title
    if parser.title:
        report.append(f"[OK] Title found: '{parser.title}' ({len(parser.title)} chars)")
        if len(parser.title) < 10 or len(parser.title) > 70:
            report.append(f"  [WARN] Title length ideal is 10-70 chars.")
    else:
        report.append(f"[CRITICAL] No <title> tag found.")

    # Meta Description
    if parser.meta_description:
        report.append(f"[OK] Meta Description found ({len(parser.meta_description)} chars).")
        if len(parser.meta_description) < 50 or len(parser.meta_description) > 160:
            report.append(f"  [WARN] Meta Description ideal length is 50-160 chars.")
    else:
        report.append(f"[WARN] No Meta Description found.")

    # Viewport
    if parser.viewport:
        report.append(f"[OK] Viewport tag present.")
    else:
        report.append(f"[CRITICAL] Viewport tag missing (Mobile responsiveness issue).")

    # H1
    if parser.h1_count == 1:
        report.append(f"[OK] Exactly one H1 tag found.")
    elif parser.h1_count == 0:
        report.append(f"[CRITICAL] No H1 tag found.")
    else:
        report.append(f"[WARN] Multiple H1 tags found ({parser.h1_count}).")

    # Content Hierarchy
    # Simple check: are there headers?
    if parser.headers:
        report.append(f"[INFO] Header structure found (First 5): {[h[0] for h in parser.headers[:5]]}...")
    else:
        report.append(f"[WARN] No headers (h1-h6) found.")

    # Images
    if parser.total_images > 0:
        if parser.images_without_alt == 0:
            report.append(f"[OK] All {parser.total_images} images have alt text.")
        else:
            report.append(f"[WARN] {parser.images_without_alt}/{parser.total_images} images missing alt text.")
    else:
        report.append(f"[INFO] No images found.")

    # Semantic HTML
    semantic_found = [tag for tag, count in parser.semantic_tags.items() if count > 0]
    if semantic_found:
        report.append(f"[OK] Semantic tags used: {', '.join(semantic_found)}")
    else:
        report.append(f"[WARN] No HTML5 semantic tags (header, main, footer, etc.) found.")

    # Canonical
    if parser.canonical:
        report.append(f"[OK] Canonical tag: {parser.canonical}")
    else:
        report.append(f"[INFO] No canonical tag.")
        
    report.append("\n")
    return "\n".join(report)

def analyze_sitemap():
    report = ["--- SITEMAP ANALYSIS: sitemap.xml ---"]
    if not os.path.exists("sitemap.xml"):
        report.append("[CRITICAL] sitemap.xml missing.")
        return "\n".join(report)

    try:
        tree = ET.parse("sitemap.xml")
        root = tree.getroot()
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('ns:url', namespace)
        report.append(f"[OK] Sitemap valid XML. Contains {len(urls)} URLs.")
        
        # Check first few
        count = 0
        for url in urls:
            loc = url.find('ns:loc', namespace).text
            if count < 3:
                report.append(f"  Entry: {loc}")
            count += 1
            
    except Exception as e:
        report.append(f"[CRITICAL] Sitemap parse error: {e}")
    
    return "\n".join(report)

if __name__ == "__main__":
    full_report = ""
    for f in FILES_TO_ANALYZE:
        full_report += analyze_file(f)
    
    full_report += analyze_sitemap()
    
    with open("analysis_results.txt", "w", encoding='utf-8') as f:
        f.write(full_report)
    
    print("Analysis complete. Saved to analysis_results.txt")

#!/usr/bin/env python3
"""
Fix Google Fonts to truly async load across all pages
"""

import re
from pathlib import Path

def fix_google_fonts(file_path):
    """Fix Google Fonts to load asynchronously"""
    content = file_path.read_text(encoding='utf-8')
    
    # Find Google Fonts link
    pattern = r'(<link rel="preconnect"[^>]*fonts\.googleapis[^>]*>\s*<link rel="preconnect"[^>]*fonts\.gstatic[^>]*>\s*)<link[^>]*href="https://fonts\.googleapis\.com/css2[^>]*>.*?(?=</noscript>|<link|<style)'
    
    # Replacement with async loading
    replacement = r'''\1<link rel="preload" as="style" onload="this.onload=null;this.rel='stylesheet'"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@400;600;800&display=swap">
    <noscript>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@400;600;800&display=swap">
    </noscript>
    '''
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        return True
    return False

# Process all pages
pages = [
    'index.html',
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-prompt-research.html',
    'report-veo-tech.html',
]

if __name__ == '__main__':
    print("🔧 Fixing Google Fonts async loading\n")
    
    success = 0
    for page_name in pages:
        file_path = Path(page_name)
        if file_path.exists():
            if fix_google_fonts(file_path):
                print(f"✅ {page_name}: Fixed font loading")
                success += 1
            else:
                print(f"ℹ️  {page_name}: Already optimized or pattern not found")
        else:
            print(f"❌ {page_name}: Not found")
    
    print(f"\n✨ Done! Fixed {success} pages")
    print("🚀 Fonts now load asynchronously with display:swap")

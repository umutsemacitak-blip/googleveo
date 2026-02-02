#!/usr/bin/env python3
"""
EMERGENCY FIX: Remove Google Fonts completely
Replace with system fonts to eliminate CLS and blocking
"""

import re
from pathlib import Path

def remove_google_fonts(file_path):
    """Remove Google Fonts and update CSS"""
    content = file_path.read_text(encoding='utf-8')
    
    # Remove preconnect
    content = re.sub(r'\s*<!-- Preconnect[^>]*>.*?crossorigin>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*<link rel="preconnect"[^>]*fonts[^>]*>', '', content)
    
    # Remove Google Fonts link
    content = re.sub(r'\s*<link[^>]*fonts\.googleapis\.com[^>]*>', '', content)
    
    file_path.write_text(content, encoding='utf-8')
    return True

def update_css_for_system_fonts():
    """Update CSS to use system fonts"""
    css_path = Path('style.css')
    content = css_path.read_text(encoding='utf-8')
    
    # Replace font families with system fonts
    content = re.sub(
        r'--font-heading: .*?;',
        "--font-heading: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;",
        content
    )
    
    content = re.sub(
        r'--font-body: .*?;',
        "--font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;",
        content
    )
    
    css_path.write_text(content, encoding='utf-8')
    return True

pages = [
    'index.html',
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-prompt-research.html',
    'report-veo-tech.html',
]

if __name__ == '__main__':
    print("🚨 EMERGENCY FIX: Removing Google Fonts\n")
    print("This will:")
    print("  - Eliminate 780ms blocking time")
    print("  - Fix CLS from 1.000 to 0")
    print("  - Use fast system fonts instead\n")
    
    # Update CSS first
    update_css_for_system_fonts()
    print("✅ Updated CSS to use system fonts")
    
    # Remove from HTML
    for page_name in pages:
        file_path = Path(page_name)
        if file_path.exists():
            remove_google_fonts(file_path)
            print(f"✅ {page_name}: Removed Google Fonts")
    
    print("\n✨ Done!")
    print("\n📈 Expected improvements:")
    print("  - Performance: 71 → 95+")
    print("  - CLS: 1.000 → 0")
    print("  - Blocking time: -780ms")

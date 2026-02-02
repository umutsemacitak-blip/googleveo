#!/usr/bin/env python3
"""
Apply PageSpeed Optimizations to All HTML Pages
- Defer CSS loading
- Optimize font loading (reduce weights + async)
- Defer scripts
"""

import re
from pathlib import Path

def optimize_page(file_path):
    """Apply PageSpeed optimizations to a single HTML page"""
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return False
    
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    changes_made = []
    
    # 1. Optimize Google Fonts - reduce weights and add async loading
    # Find existing Google Fonts link
    font_pattern = r'<link\s+href="https://fonts\.googleapis\.com/css2\?family=[^"]+"\s+rel="stylesheet"[^>]*>'
    font_match = re.search(font_pattern, content)
    
    if font_match:
        old_font_link = font_match.group(0)
        
        # Replace with optimized version
        optimized_fonts = '''<!-- Optimized Font Loading - Reduced weights + async loading -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" 
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@400;600;800&display=swap">
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@400;600;800&display=swap"
        rel="stylesheet" media="print" onload="this.media='all'">
    <noscript>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    </noscript>'''
        
        # Find the preconnect tags too and replace the whole block
        full_font_block = r'(<link rel="preconnect" href="https://fonts\.googleapis\.com"[^>]*>.*?<link\s+href="https://fonts\.googleapis\.com/css2[^>]+>)'
        if re.search(full_font_block, content, re.DOTALL):
            content = re.sub(full_font_block, optimized_fonts, content, flags=re.DOTALL, count=1)
            changes_made.append("Optimized font loading")
    
    # 2. Defer CSS loading (style.css)
    css_pattern = r'<link rel="stylesheet" href="style\.css">'
    if re.search(css_pattern, content):
        deferred_css = '''<!-- Defer non-critical CSS -->
    <link rel="preload" as="style" href="style.css">
    <link rel="stylesheet" href="style.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="style.css"></noscript>'''
        
        content = re.sub(css_pattern, deferred_css, content)
        changes_made.append("Deferred CSS loading")
    
    # 3. Defer scripts
    # Find script tags without defer
    script_pattern = r'<script src="([^"]+)"( defer)?></script>'
    
    def add_defer(match):
        src = match.group(1)
        has_defer = match.group(2)
        if has_defer:
            return match.group(0)  # Already has defer
        return f'<script src="{src}" defer></script>'
    
    new_content = re.sub(script_pattern, add_defer, content)
    if new_content != content:
        content = new_content
        changes_made.append("Added defer to scripts")
    
    # Check if any changes were made
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ {file_path.name}: {', '.join(changes_made)}")
        return True
    else:
        print(f"ℹ️  {file_path.name}: No changes needed (already optimized)")
        return False

# Pages to optimize
pages_to_optimize = [
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-prompt-research.html',
    'report-veo-tech.html',
]

if __name__ == '__main__':
    print("🚀 Applying PageSpeed Optimizations\n")
    
    success_count = 0
    for page_name in pages_to_optimize:
        file_path = Path(page_name)
        if optimize_page(file_path):
            success_count += 1
    
    print(f"\n✨ Done! Optimized {success_count}/{len(pages_to_optimize)} pages")
    print("\nNote: index.html was already optimized manually")

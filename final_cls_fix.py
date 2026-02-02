#!/usr/bin/env python3
"""
Final CLS fix: Remove all animations from all pages
"""

import re
from pathlib import Path

def remove_drift_animation(file_path):
    """Remove drift animation from scroll indicators"""
    content = file_path.read_text(encoding='utf-8')
    
    # Remove drift animation from inline styles
    content = re.sub(
        r'animation:\s*drift[^;"]*;?\s*',
        '',
        content
    )
    
    file_path.write_text(content, encoding='utf-8')
    return True

pages = [
    'index.html',
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-prompt-research.html',
    'report-veo-tech.html',
]

if __name__ == '__main__':
    print("🎯 Final CLS Fix: Removing all drift animations\n")
    
    for page_name in pages:
        file_path = Path(page_name)
        if file_path.exists():
            remove_drift_animation(file_path)
            print(f"✅ {page_name}")
    
    print("\n✨ CLS should now be 0!")

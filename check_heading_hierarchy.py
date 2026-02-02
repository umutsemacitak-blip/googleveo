#!/usr/bin/env python3
"""
Fix Heading Hierarchy Issues
Ensure headings follow sequential order (h1 -> h2 -> h3, etc.)
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def analyze_heading_hierarchy(file_path):
    """Analyze heading structure in HTML file"""
    if not file_path.exists():
        return None
    
    content = file_path.read_text(encoding='utf-8')
    
    # Find all headings
    headings = []
    for level in range(1, 7):
        pattern = rf'<h{level}[^>]*>(.*?)</h{level}>'
        matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            text = re.sub(r'<[^>]+>', '', match.group(1)).strip()[:50]
            headings.append((level, text, match.start()))
    
    # Sort by position
    headings.sort(key=lambda x: x[2])
    
    return [(h[0], h[1]) for h in headings]

def check_hierarchy_issues(headings):
    """Check for hierarchy issues"""
    if not headings:
        return []
    
    issues = []
    prev_level = 0
    
    for i, (level, text) in enumerate(headings):
        # Issue 1: Multiple H1s
        if level == 1 and i > 0 and headings[i-1][0] == 1:
            issues.append(f"Multiple H1 tags ('{text}')")
        
        # Issue 2: Skipped levels
        if prev_level > 0 and level > prev_level + 1:
            issues.append(f"Skipped from H{prev_level} to H{level} ('{text}')")
        
        prev_level = level
    
    return issues

# Analyze all HTML pages
pages = [
    'index.html',
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-prompt-research.html',
    'report-veo-tech.html',
    '10PhaseAuthorityBlueprintMasteringGoogleVeo3i.html',
    'GoogleVeo3SEOMakaleretimi.html',
    'GoogleVeoPromptEngineeringResearch.html'
]

if __name__ == '__main__':
    print("📋 Heading Hierarchy Analysis\n")
    
    total_issues = 0
    
    for page_name in pages:
        file_path = Path(page_name)
        headings = analyze_heading_hierarchy(file_path)
        
        if headings is None:
            print(f"❌ {page_name}: File not found")
            continue
        
        issues = check_hierarchy_issues(headings)
        
        if issues:
            print(f"⚠️  {page_name}:")
            for issue in issues:
                print(f"   - {issue}")
                total_issues += 1
        else:
            print(f"✅ {page_name}: Good hierarchy")
        
        # Show structure
        if headings:
            structure = " -> ".join([f"H{h[0]}" for h in headings[:5]])
            if len(headings) > 5:
                structure += f" ... ({len(headings)} total)"
            print(f"   Structure: {structure}")
        print()
    
    if total_issues == 0:
        print("✨ All pages have correct heading hierarchy!")
    else:
        print(f"⚠️  Found {total_issues} heading hierarchy issues")
        print("Note: Some issues may be acceptable (e.g., multiple sections with different H1s)")

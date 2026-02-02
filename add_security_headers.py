#!/usr/bin/env python3
"""
Add Security Headers and Favicon to all HTML pages
"""

import re
from pathlib import Path

# Security headers as meta tags (HTML-based CSP)
SECURITY_HEADERS = '''    <!-- Security Headers -->
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com https://fonts.googleapis.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="alternate icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="favicon.svg">
'''

def add_security_and_favicon(file_path):
    """Add security headers and favicon to HTML file"""
    content = file_path.read_text(encoding='utf-8')
    
    # Check if already added
    if 'Content-Security-Policy' in content:
        return False
    
    # Find <head> tag and add after it or after charset
    pattern = r'(<meta charset="[^"]+">)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1\n' + SECURITY_HEADERS, content, count=1)
        file_path.write_text(content, encoding='utf-8')
        return True
    
    return False

# Process all HTML files
html_files = [
    'index.html',
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-prompt-research.html',
    'report-veo-tech.html',
]

if __name__ == '__main__':
    print("🔒 Adding Security Headers & Favicon\n")
    
    success = 0
    for filename in html_files:
        file_path = Path(filename)
        if file_path.exists():
            if add_security_and_favicon(file_path):
                print(f"✅ {filename}: Added security headers & favicon")
                success += 1
            else:
                print(f"ℹ️  {filename}: Already has security headers")
        else:
            print(f"❌ {filename}: Not found")
    
    print(f"\n✨ Done! Modified {success} files")
    print("\n📌 Security improvements added:")
    print("  - CSP (Content Security Policy)")
    print("  - X-Frame-Options (Clickjacking protection)")
    print("  - X-Content-Type-Options")
    print("  - Referrer Policy")
    print("  - L1 Favicon (SVG)")

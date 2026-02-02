#!/usr/bin/env python3
"""
Remove meta security headers that don't work
Meta tags can't set X-Frame-Options or frame-ancestors
"""

import re
from pathlib import Path

def remove_ineffective_security_meta(file_path):
    """Remove security meta tags that don't work in meta"""
    content = file_path.read_text(encoding='utf-8')
    
    # Remove the CSP and security meta tags block
    pattern = r'\s*<!-- Security Headers -->.*?<!-- Favicon -->'
    content = re.sub(pattern, '\n    <!-- Favicon -->', content, flags=re.DOTALL)
    
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
    print("🔧 Removing ineffective meta security headers\n")
    print("Note: These headers only work via HTTP server, not meta tags\n")
    
    for page_name in pages:
        file_path = Path(page_name)
        if file_path.exists():
            remove_ineffective_security_meta(file_path)
            print(f"✅ {page_name}: Removed ineffective meta headers")
    
    print("\n✨ Done!")
    print("\n📝 Server-side headers needed:")
    print("  Strict-Transport-Security: max-age=31536000")
    print("  X-Frame-Options: DENY")
    print("  X-Content-Type-Options: nosniff")
    print("  Cross-Origin-Opener-Policy: same-origin")

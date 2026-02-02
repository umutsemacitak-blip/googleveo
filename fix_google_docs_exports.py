#!/usr/bin/env python3
"""
Fix Google Docs Export Files - Add Complete SEO
These files have NO SEO elements at all
"""

import re
from pathlib import Path

def fix_google_docs_export(filename, title, description):
    """Fix a Google Docs exported HTML file"""
    file_path = Path(filename)
    
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return False
    
    content = file_path.read_text(encoding='utf-8')
    
    # These files start with <html><head><meta content="text/html; charset=UTF-8"...
    # We need to inject proper SEO after the charset meta
    
    # 1. Add viewport meta after charset
    viewport_meta = '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
    content = re.sub(
        r'(<meta content="text/html; charset=UTF-8" http-equiv="content-type">)',
        r'\1' + viewport_meta,
        content
    )
    
    # 2. Add title and description before <style>
    seo_tags = f'''
    <title>{title}</title>
    <meta name="description" content="{description}">
    
    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="BQ5M Labs">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
'''

    content = re.sub(
        r'(<meta name="viewport"[^>]*>)',
        r'\1' + seo_tags,
        content
    )
    
    # 3. Add simple footer with social links before </body>
    social_footer = '''
    
    <!-- Social Media Footer -->
    <div style="max-width: 800px; margin: 4rem auto 0; padding: 2rem; border-top: 2px solid #e0e0e0; text-align: center;">
        <h2 style="font-size: 1.5rem; margin-bottom: 1rem; color: #333;">Connect with BQ5M Labs</h2>
        <div style="display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem;">
            <a href="https://www.linkedin.com/in/umutcitak/" target="_blank" rel="noopener" 
               style="color: #0077b5; text-decoration: none; font-size: 1.1rem; font-weight: 500;">
                🔗 LinkedIn
            </a>
            <a href="https://web.telegram.org/a/#7972155176" target="_blank" rel="noopener"
               style="color: #0088cc; text-decoration: none; font-size: 1.1rem; font-weight: 500;">
                ✈️ Telegram
            </a>
            <a href="https://g.dev/umutcitak" target="_blank" rel="noopener"
               style="color: #4285f4; text-decoration: none; font-size: 1.1rem; font-weight: 500;">
                🚀 Google Developer
            </a>
        </div>
        <p style="margin-top: 2rem; color: #666; font-size: 0.9rem;">
            <strong>Umut Çıtak</strong> | info@bq5m.com | Çukurambar Next Level 105/A34-7165, Ankara, TR
        </p>
    </div>
'''
    
    content = re.sub(
        r'(</body>)',
        social_footer + r'\n\1',
        content
    )
    
    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Fixed {file_path.name}")
    return True

# File configurations
files_to_fix = [
    {
        'filename': '10PhaseAuthorityBlueprintMasteringGoogleVeo3i.html',
        'title': 'Google Veo 3: 10-Phase Authority Blueprint for Education',
        'description': 'The 10-Phase Authority Blueprint for Google Veo 3 in Education: Master technical architecture, SEO dominance, JSON prompts, API implementation, and advanced pedagogical workflows for AI video generation.'
    },
    {
        'filename': 'GoogleVeo3SEOMakaleretimi.html',
        'title': 'Google Veo 3 SEO Content Creation: Technical Guide',
        'description': 'Comprehensive guide to Google Veo 3 SEO content creation: Advanced techniques for search engine optimization, keyword integration strategies, content workflows, and video generation for maximum visibility.'
    },
    {
        'filename': 'GoogleVeoPromptEngineeringResearch.html',
        'title': 'Google Veo Prompt Engineering: Advanced Research Guide',
        'description': 'In-depth Google Veo prompt engineering research: Advanced JSON formulas, cinematography patterns, lighting controls, physics simulation techniques, and visual direction workflows for professional video generation.'
    }
]

if __name__ == '__main__':
    print("🔧 Fixing Google Docs Export Files\n")
    
    success_count = 0
    for config in files_to_fix:
        if fix_google_docs_export(config['filename'], config['title'], config['description']):
            success_count += 1
    
    print(f"\n✨ Done! Fixed {success_count}/{len(files_to_fix)} files")

#!/usr/bin/env python3
"""
Batch SEO Fixer for Remaining Report Pages
Adds H1, extends meta descriptions, adds Open Graph tags, and adds social media links
"""

import re
from pathlib import Path

# Social media links template
SOCIAL_LINKS_HTML = '''
                            <!-- Social Media Links -->
                            <div class="contact-item" style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1);">
                                <div class="c-detail" style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
                                    <a href="https://www.linkedin.com/in/umutcitak/" class="social-link" target="_blank" rel="noopener" 
                                       style="display: flex; align-items: center; gap: 0.5rem; color: var(--neon-cyan); text-decoration: none; transition: all 0.3s ease;">
                                        <i class="ph-fill ph-linkedin-logo" style="font-size: 1.5rem;"></i>
                                        <span class="c-label">LinkedIn</span>
                                    </a>
                                    <a href="https://web.telegram.org/a/#7972155176" class="social-link" target="_blank" rel="noopener"
                                       style="display: flex; align-items: center; gap: 0.5rem; color: var(--neon-cyan); text-decoration: none; transition: all 0.3s ease;">
                                        <i class="ph-fill ph-telegram-logo" style="font-size: 1.5rem;"></i>
                                        <span class="c-label">Telegram</span>
                                    </a>
                                    <a href="https://g.dev/umutcitak" class="social-link" target="_blank" rel="noopener"
                                       style="display: flex; align-items: center; gap: 0.5rem; color: var(--neon-cyan); text-decoration: none; transition: all 0.3s ease;">
                                        <i class="ph-fill ph-google-logo" style="font-size: 1.5rem;"></i>
                                        <span class="c-label">Google Developer</span>
                                    </a>
                                </div>
                            </div>'''

def create_og_tags(title, description, url):
    """Create Open Graph meta tags"""
    return f'''    
    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="BQ5M Labs">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">'''

def fix_report_prompt_research():
    """Fix report-prompt-research.html"""
    file_path = Path('report-prompt-research.html')
    
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return
    
    content = file_path.read_text(encoding='utf-8')
    
    # 1. Extend title (currently 53 chars - good, but add keywords)
    new_title = "Google Veo Prompt Engineering: Advanced Research & Analysis"
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{new_title}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 2. Extend meta description
    new_desc = "Comprehensive Google Veo prompt engineering research: Advanced JSON formulas, cinematography patterns, lighting controls, physics simulation techniques, and visual direction workflows for optimal video generation."
    content = re.sub(
        r'<meta name="description" content=".*?"',
        f'<meta name="description" content="{new_desc}"',
        content
    )
    
    # 3. Add Open Graph tags after title
    og_tags = create_og_tags(new_title, new_desc, "https://bq5m.com/report-prompt-research.html")
    content = re.sub(
        r'(<title>.*?</title>)',
        r'\1' + og_tags,
        content,
        flags=re.DOTALL
    )
    
    # 4. Add H1 wrapper before article content
    h1_wrapper = '''                <!-- H1 Wrapper for SEO -->
                <div style="margin-bottom:2rem;">
                    <h1 style="font-size:2.5rem; color:var(--neon-cyan); margin-bottom:0.5rem;">Google Veo Prompt Engineering Research</h1>
                    <p style="color:rgba(255,255,255,0.7); font-size:1rem;">Advanced Analysis & Optimization Techniques</p>
                </div>
                '''
    
    # Find the article-body div and add H1 before it
    content = re.sub(
        r'(<div id="google-report-\d+" class="article-body")',
        h1_wrapper + r'\1',
        content
    )
    
    # 5. Add social links before closing contact section
    patterns_to_find = [
        (r'(</div>\s*</div>\s*<div class="map-abstract">)', SOCIAL_LINKS_HTML + r'\n                        \1'),
        (r'(</div>\s*</div>\s*</section>\s*</main>)', SOCIAL_LINKS_HTML + r'\n                        \1'),
    ]
    
    for pattern, replacement in patterns_to_find:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content, count=1)
            break
    
    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Fixed {file_path.name}")

def fix_report_veo_tech():
    """Fix report-veo-tech.html"""
    file_path = Path('report-veo-tech.html')
    
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return
    
    content = file_path.read_text(encoding='utf-8')
    
    # 1. Extend title
    new_title = "Google Veo 3.1 Technical Deep Dive: Architecture & Analysis"
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{new_title}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 2. Extend meta description
    new_desc = "Comprehensive technical analysis of Google Veo 3.1: Advanced architecture breakdown, 4K upscaling capabilities, motion physics engine, benchmark comparisons vs Sora 2, API implementation guides, and performance optimization strategies."
    content = re.sub(
        r'<meta name="description" content=".*?"',
        f'<meta name="description" content="{new_desc}"',
        content
    )
    
    # 3. Add Open Graph tags
    og_tags = create_og_tags(new_title, new_desc, "https://bq5m.com/report-veo-tech.html")
    content = re.sub(
        r'(<title>.*?</title>)',
        r'\1' + og_tags,
        content,
        flags=re.DOTALL
    )
    
    # 4. Add H1 wrapper
    h1_wrapper = '''                <!-- H1 Wrapper for SEO -->
                <div style="margin-bottom:2rem;">
                    <h1 style="font-size:2.5rem; color:var(--neon-cyan); margin-bottom:0.5rem;">Google Veo 3.1 Technical Deep Dive</h1>
                    <p style="color:rgba(255,255,255,0.7); font-size:1rem;">Architecture, Performance & Advanced Capabilities</p>
                </div>
                '''
    
    content = re.sub(
        r'(<div id="google-report-\d+" class="article-body")',
        h1_wrapper + r'\1',
        content
    )
    
    # 5. Add social links
    patterns_to_find = [
        (r'(</div>\s*</div>\s*<div class="map-abstract">)', SOCIAL_LINKS_HTML + r'\n                        \1'),
        (r'(</div>\s*</div>\s*</section>\s*</main>)', SOCIAL_LINKS_HTML + r'\n                        \1'),
    ]
    
    for pattern, replacement in patterns_to_find:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content, count=1)
            break
    
    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Fixed {file_path.name}")

if __name__ == '__main__':
    print("🔧 Batch SEO Fixer for Report Pages\n")
    fix_report_prompt_research()
    fix_report_veo_tech()
    print("\n✨ Done!")

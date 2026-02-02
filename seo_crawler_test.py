#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Crawler Visibility Test
Google botlarının içeriği nasıl gördüğünü test eder
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
import json

class SEOAnalyzer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_tags = []
        self.headings = defaultdict(list)
        self.images = []
        self.links = []
        self.structured_data = []
        self.text_content = []
        self.issues = []
        self.current_tag = None
        self.title = ""
        self.in_script = False
        self.in_style = False
        self.in_noscript = False
        self.hidden_content = []
        self.semantic_tags = defaultdict(int)
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag
        
        # Track semantic HTML5 tags
        semantic = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        if tag in semantic:
            self.semantic_tags[tag] += 1
        
        # Meta tags
        if tag == 'meta':
            self.meta_tags.append(attrs_dict)
            
        # Title
        elif tag == 'title':
            pass  # Will be handled in handle_data
            
        # Headings
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_heading = tag
            
        # Images
        elif tag == 'img':
            img_info = {
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt', ''),
                'loading': attrs_dict.get('loading', 'eager')
            }
            self.images.append(img_info)
            if not img_info['alt']:
                self.issues.append(f"⚠️ Image without alt text: {img_info['src'][:50]}")
                
        # Links
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            self.links.append({
                'href': href,
                'rel': attrs_dict.get('rel', ''),
                'text': ''  # Will be filled in handle_data
            })
            
        # Scripts
        elif tag == 'script':
            self.in_script = True
            script_type = attrs_dict.get('type', 'text/javascript')
            if script_type == 'application/ld+json':
                pass  # Structured data, will be collected
                
        # Style
        elif tag == 'style':
            self.in_style = True
            
        # Noscript
        elif tag == 'noscript':
            self.in_noscript = True
            
        # Check for hidden content
        style = attrs_dict.get('style', '')
        css_class = attrs_dict.get('class', '')
        if 'display:none' in style.replace(' ', '') or 'visibility:hidden' in style.replace(' ', ''):
            self.hidden_content.append(f"Hidden element: <{tag} class='{css_class}'>")
            
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag == 'noscript':
            self.in_noscript = False
        self.current_tag = None
            
    def handle_data(self, data):
        # Skip script and style content
        if self.in_script or self.in_style:
            return
            
        data = data.strip()
        if not data:
            return
            
        # Title
        if self.current_tag == 'title':
            self.title = data
            
        # Headings
        elif self.current_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.headings[self.current_tag].append(data)
            
        # Regular text content (visible to crawlers)
        elif not self.in_noscript:
            if len(data) > 10:  # Only meaningful text
                self.text_content.append(data)

def analyze_html_file(file_path):
    """Analyze a single HTML file for SEO"""
    print(f"\n{'='*80}")
    print(f"📄 Analyzing: {os.path.basename(file_path)}")
    print(f"{'='*80}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    analyzer = SEOAnalyzer()
    analyzer.feed(html_content)
    
    results = {
        'file': os.path.basename(file_path),
        'issues': [],
        'warnings': [],
        'success': [],
        'stats': {}
    }
    
    # 1. Title Tag
    print("\n🏷️  TITLE TAG")
    if analyzer.title:
        title_len = len(analyzer.title)
        print(f"   ✅ Title: {analyzer.title[:70]}...")
        print(f"   📏 Length: {title_len} characters", end="")
        if 50 <= title_len <= 60:
            print(" (Optimal ✅)")
            results['success'].append(f"Title length optimal: {title_len} chars")
        elif title_len < 50:
            print(" (Too short ⚠️)")
            results['warnings'].append(f"Title too short: {title_len} chars (recommend 50-60)")
        else:
            print(" (Too long ⚠️)")
            results['warnings'].append(f"Title too long: {title_len} chars (recommend 50-60)")
    else:
        print("   ❌ NO TITLE TAG FOUND!")
        results['issues'].append("Missing title tag")
    
    # 2. Meta Description
    print("\n📝 META DESCRIPTION")
    meta_desc = None
    for meta in analyzer.meta_tags:
        if meta.get('name', '').lower() == 'description':
            meta_desc = meta.get('content', '')
            break
    
    if meta_desc:
        desc_len = len(meta_desc)
        print(f"   ✅ Description: {meta_desc[:100]}...")
        print(f"   📏 Length: {desc_len} characters", end="")
        if 150 <= desc_len <= 160:
            print(" (Optimal ✅)")
            results['success'].append(f"Meta description length optimal: {desc_len} chars")
        elif desc_len < 150:
            print(" (Too short ⚠️)")
            results['warnings'].append(f"Meta description too short: {desc_len} chars")
        else:
            print(" (Too long ⚠️)")
            results['warnings'].append(f"Meta description too long: {desc_len} chars")
    else:
        print("   ❌ NO META DESCRIPTION FOUND!")
        results['issues'].append("Missing meta description")
    
    # 3. Meta Keywords (optional but good to know)
    print("\n🔑 META KEYWORDS")
    meta_keywords = None
    for meta in analyzer.meta_tags:
        if meta.get('name', '').lower() == 'keywords':
            meta_keywords = meta.get('content', '')
            break
    
    if meta_keywords:
        print(f"   ℹ️  Keywords: {meta_keywords[:100]}...")
        results['success'].append("Meta keywords present")
    else:
        print("   ⚠️  No meta keywords (optional)")
    
    # 4. Open Graph Tags
    print("\n📱 OPEN GRAPH TAGS (Social Media)")
    og_tags = [meta for meta in analyzer.meta_tags if meta.get('property', '').startswith('og:')]
    if og_tags:
        for og in og_tags[:5]:
            print(f"   ✅ {og.get('property')}: {og.get('content', '')[:50]}...")
        results['success'].append(f"Open Graph tags present: {len(og_tags)} tags")
    else:
        print("   ⚠️  No Open Graph tags (recommended for social sharing)")
        results['warnings'].append("Missing Open Graph tags")
    
    # 5. Heading Structure
    print("\n📋 HEADING STRUCTURE")
    h1_count = len(analyzer.headings.get('h1', []))
    print(f"   H1: {h1_count} found")
    
    if h1_count == 0:
        print("      ❌ NO H1 FOUND! Critical SEO issue!")
        results['issues'].append("Missing H1 heading")
    elif h1_count == 1:
        print(f"      ✅ Perfect! H1: {analyzer.headings['h1'][0][:60]}...")
        results['success'].append(f"Single H1 tag present")
    else:
        print(f"      ⚠️  Multiple H1 tags (not recommended)")
        results['warnings'].append(f"Multiple H1 tags: {h1_count}")
    
    for h_level in ['h2', 'h3', 'h4']:
        count = len(analyzer.headings.get(h_level, []))
        if count > 0:
            print(f"   {h_level.upper()}: {count} found")
            if count >= 1:
                print(f"      ✅ {analyzer.headings[h_level][0][:60]}...")
    
    # 6. Content Analysis
    print("\n📖 CONTENT VISIBILITY (Bot View)")
    total_text = ' '.join(analyzer.text_content)
    word_count = len(total_text.split())
    print(f"   📊 Total visible words: {word_count}")
    
    if word_count < 300:
        print("   ⚠️  Low content (recommend 300+ words for SEO)")
        results['warnings'].append(f"Low word count: {word_count} words")
    else:
        print("   ✅ Good content volume")
        results['success'].append(f"Good word count: {word_count} words")
    
    # Show sample content
    print(f"\n   📄 Content Preview (first 200 chars):")
    print(f"   {total_text[:200]}...")
    
    # 7. Image Optimization
    print(f"\n🖼️  IMAGES")
    print(f"   Total images: {len(analyzer.images)}")
    images_without_alt = sum(1 for img in analyzer.images if not img['alt'])
    if images_without_alt > 0:
        print(f"   ❌ Images without ALT text: {images_without_alt}")
        results['issues'].append(f"{images_without_alt} images missing alt text")
    else:
        print(f"   ✅ All images have ALT text")
        results['success'].append("All images have alt text")
    
    lazy_loading = sum(1 for img in analyzer.images if img['loading'] == 'lazy')
    if lazy_loading > 0:
        print(f"   ✅ Lazy loading enabled: {lazy_loading} images")
        results['success'].append(f"Lazy loading on {lazy_loading} images")
    
    # 8. Links
    print(f"\n🔗 LINKS")
    print(f"   Total links: {len(analyzer.links)}")
    internal_links = sum(1 for link in analyzer.links if not link['href'].startswith('http'))
    external_links = len(analyzer.links) - internal_links
    print(f"   Internal: {internal_links}, External: {external_links}")
    
    # 9. Semantic HTML5
    print(f"\n🏗️  SEMANTIC HTML5 STRUCTURE")
    if analyzer.semantic_tags:
        for tag, count in analyzer.semantic_tags.items():
            print(f"   ✅ <{tag}>: {count}")
        results['success'].append("Semantic HTML5 tags used")
    else:
        print("   ⚠️  No semantic HTML5 tags found (use <header>, <nav>, <main>, etc.)")
        results['warnings'].append("Missing semantic HTML5 tags")
    
    # 10. Hidden Content Warning
    if analyzer.hidden_content:
        print(f"\n⚠️  HIDDEN CONTENT (May not be indexed)")
        for item in analyzer.hidden_content[:5]:
            print(f"   {item}")
        results['warnings'].append(f"{len(analyzer.hidden_content)} hidden elements")
    
    # 11. Mobile Optimization
    print(f"\n📱 MOBILE OPTIMIZATION")
    viewport_meta = None
    for meta in analyzer.meta_tags:
        if meta.get('name', '').lower() == 'viewport':
            viewport_meta = meta.get('content', '')
            break
    
    if viewport_meta:
        print(f"   ✅ Viewport meta tag: {viewport_meta}")
        results['success'].append("Viewport meta tag present")
    else:
        print("   ❌ NO VIEWPORT META TAG! Critical for mobile SEO!")
        results['issues'].append("Missing viewport meta tag")
    
    # 12. Canonical URL
    print(f"\n🔗 CANONICAL URL")
    has_canonical = False
    for meta in analyzer.meta_tags:
        if meta.get('rel', '') == 'canonical':
            print(f"   ✅ Canonical: {meta.get('href', '')}")
            has_canonical = True
            results['success'].append("Canonical URL set")
            break
    
    if not has_canonical:
        print("   ℹ️  No canonical URL (optional but recommended)")
    
    # Stats
    results['stats'] = {
        'word_count': word_count,
        'images': len(analyzer.images),
        'links': len(analyzer.links),
        'h1_count': h1_count,
        'title_length': len(analyzer.title) if analyzer.title else 0,
        'meta_desc_length': len(meta_desc) if meta_desc else 0
    }
    
    return results

def generate_summary_report(all_results):
    """Generate a summary report for all files"""
    print(f"\n\n{'='*80}")
    print("📊 OVERALL SEO SUMMARY REPORT")
    print(f"{'='*80}\n")
    
    total_files = len(all_results)
    total_issues = sum(len(r['issues']) for r in all_results)
    total_warnings = sum(len(r['warnings']) for r in all_results)
    
    print(f"📁 Files analyzed: {total_files}")
    print(f"❌ Critical issues: {total_issues}")
    print(f"⚠️  Warnings: {total_warnings}")
    
    # Critical issues by file
    if total_issues > 0:
        print(f"\n❌ CRITICAL ISSUES TO FIX:")
        for result in all_results:
            if result['issues']:
                print(f"\n   📄 {result['file']}:")
                for issue in result['issues']:
                    print(f"      • {issue}")
    
    # Warnings
    if total_warnings > 0:
        print(f"\n⚠️  WARNINGS (Recommended to fix):")
        for result in all_results:
            if result['warnings']:
                print(f"\n   📄 {result['file']}:")
                for warning in result['warnings'][:3]:  # Show first 3
                    print(f"      • {warning}")
    
    # Success summary
    print(f"\n✅ WHAT'S WORKING WELL:")
    common_successes = defaultdict(int)
    for result in all_results:
        for success in result['success']:
            # Generalize success messages
            if 'word count' in success.lower():
                common_successes['Good content volume'] += 1
            elif 'alt text' in success.lower():
                common_successes['Images have alt text'] += 1
            elif 'viewport' in success.lower():
                common_successes['Mobile viewport configured'] += 1
            elif 'semantic' in success.lower():
                common_successes['Semantic HTML5 used'] += 1
    
    for success, count in sorted(common_successes.items(), key=lambda x: x[1], reverse=True):
        print(f"   ✅ {success}: {count}/{total_files} pages")
    
    # Stats comparison
    print(f"\n📈 CONTENT STATISTICS:")
    print(f"   {'File':<40} {'Words':<10} {'Images':<10} {'Links':<10}")
    print(f"   {'-'*70}")
    for result in all_results:
        stats = result['stats']
        filename = result['file'][:38]
        print(f"   {filename:<40} {stats['word_count']:<10} {stats['images']:<10} {stats['links']:<10}")
    
    # Final verdict
    print(f"\n{'='*80}")
    if total_issues == 0 and total_warnings < 5:
        print("🎉 VERDICT: Excellent! Your site is well-optimized for Google crawlers!")
    elif total_issues == 0:
        print("✅ VERDICT: Good! Minor improvements recommended.")
    else:
        print("⚠️  VERDICT: Action needed! Fix critical issues for better SEO.")
    print(f"{'='*80}\n")
    
    return {
        'total_files': total_files,
        'total_issues': total_issues,
        'total_warnings': total_warnings,
        'all_results': all_results
    }

def main():
    """Main function"""
    print("🔍 SEO Crawler Visibility Test")
    print("Testing how Google bots see your content...\n")
    
    # Get all HTML files
    project_dir = Path(__file__).parent
    html_files = list(project_dir.glob('*.html'))
    
    if not html_files:
        print("❌ No HTML files found!")
        return
    
    print(f"Found {len(html_files)} HTML files to analyze\n")
    
    # Analyze each file
    all_results = []
    for html_file in html_files:
        try:
            result = analyze_html_file(html_file)
            all_results.append(result)
        except Exception as e:
            print(f"❌ Error analyzing {html_file.name}: {e}")
    
    # Generate summary
    summary = generate_summary_report(all_results)
    
    # Save detailed report
    report_file = project_dir / 'seo_analysis_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed report saved to: {report_file.name}")
    print("\n✨ Analysis complete!")

if __name__ == '__main__':
    main()

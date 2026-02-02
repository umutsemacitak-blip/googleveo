#!/usr/bin/env python3
"""
Inject Prompt Data into <noscript> tag for SEO
Ensures Google Bot indexes all prompts even without executing JavaScript
"""

import json
import re
from pathlib import Path

def parse_prompt_data(data_js_path):
    """
    Extract prompt data from data.js
    Assumes format: const promptData = { ... };
    """
    try:
        content = data_js_path.read_text(encoding='utf-8')
        # Extract the JSON-like object
        # Finding the start
        start_marker = "const promptData = "
        start_idx = content.find(start_marker)
        if start_idx == -1:
            return None
        
        start_idx += len(start_marker)
        
        # Finding the end (assuming it ends with semicolon or end of file)
        # Simple extraction strategy: find the matching closing brace is hard with regex
        # But since valid JS object usually allows loose JSON, we might need a safer way or just eval it?
        # Eval is dangerous. Let's try to extract the block.
        
        # Taking everything until the last semicolon might work if the file only contains this
        json_str = content[start_idx:].strip().rstrip(';')
        
        # JS object keys might not be quoted, but usually data dumps are.
        # Let's hope it is standard JSON format. 
        # If keys are unquoted, basic json.loads will fail.
        
        # Let's clean it up to be valid JSON if needed (add quotes to keys if missing)
        # Actually, let's just use execution to dump it to json if python can't parse it easily
        # But creating a node script is dependency heavy.
        
        # Let's try simple json loads first.
        return json.loads(json_str)

    except Exception as e:
        print(f"Error parsing JSON directly: {e}")
        # Build a safe fallback using regex to extract strings if JSON fails
        # Pattern to find lists of strings
        # "Category": ["Item 1", "Item 2"]
        return extract_with_regex(content)

def extract_with_regex(content):
    """Fallback extraction"""
    data = {}
    # Find broad category blocks
    # This is a heuristic
    return {} # Placeholder, let's try not to fail first

def generate_noscript_html(data):
    """Generate SEO-friendly HTML structure"""
    html = ['<noscript>', '<div class="seo-archive">', '<h1>Veo Prompt Library Archive</h1>']
    
    total_prompts = 0
    
    for category, prompts in data.items():
        if not prompts: continue
        
        html.append(f'<h2>{category}</h2>')
        html.append('<ul>')
        for prompt in prompts:
            if isinstance(prompt, str):
                html.append(f'<li>{prompt}</li>')
                total_prompts += 1
        html.append('</ul>')
        
    html.append('</div>')
    html.append('</noscript>')
    
    return '\n'.join(html), total_prompts

def inject_into_html(html_path, noscript_content):
    content = html_path.read_text(encoding='utf-8')
    
    # Remove existing noscript prompt archive if any
    content = re.sub(r'<noscript>\s*<div class="seo-archive">.*?</noscript>', '', content, flags=re.DOTALL)
    
    # Insert before closing body
    if '</body>' in content:
        new_content = content.replace('</body>', f'{noscript_content}\n</body>')
        html_path.write_text(new_content, encoding='utf-8')
        return True
    return False

if __name__ == '__main__':
    print("🕷️ Generating SEO Noscript Fallback...")
    
    data_path = Path('data.js')
    html_path = Path('tool-prompt-library.html')
    
    if not data_path.exists() or not html_path.exists():
        print("❌ Files not found")
        exit(1)
        
    # Read JS content to manually parse since it's JS, not pure JSON
    # Since we can't easily parse partial JS in Python without libraries, 
    # we will read the file and do a clever string manipulation
    js_content = data_path.read_bytes().decode('utf-8')
    
    # Simple strategy: Use the regex to find strings array under keys
    # data.js likely has structure: "Key": [ ... ]
    # We will assume it is valid JSON syntax inside the variable assignment
    
    json_part = js_content.split('const promptData =')[1].strip()
    if json_part.endswith(';'):
        json_part = json_part[:-1]
        
    try:
        data = json.loads(json_part)
        print("✅ Successfully parsed data.js as JSON")
    except json.JSONDecodeError:
        print("⚠️  data.js is not strict JSON. User might need to check format.")
        # Attempt to clean it (e.g. trailing commas)
        # This is a "best effort" fix
        import ast
        try:
            # ast.literal_eval handles python dictionary syntax which is close to JS objects
            # but JS true/false is true/false, Python is True/False.
            # Null is None.
            py_syntax = json_part.replace('true', 'True').replace('false', 'False').replace('null', 'None')
            data = ast.literal_eval(py_syntax)
            print("✅ Parsed using AST literal evaluation")
        except Exception as e:
            print(f"❌ Failed to parse data: {e}")
            exit(1)
            
    noscript_html, count = generate_noscript_html(data)
    
    if inject_into_html(html_path, noscript_html):
        print(f"✅ Injected {count} prompts into {html_path.name}")
        print("   Google Bot can now see ALL prompts without JavaScript!")
    else:
        print("❌ Failed to inject content")

import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path

def simulate_google_bot(file_path):
    print(f"\n🕷️ Testing: {file_path.name}")
    content = file_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    # 1. Check if Content is in HTML (view-source)
    # Raporlar için ideal olan budur
    text_content = soup.get_text()
    
    # 2. Check key sections
    has_h1 = bool(soup.find('h1'))
    word_count = len(text_content.split())
    
    print(f"   - Visible Word Count (Static HTML): {word_count}")
    print(f"   - H1 Tag Found: {'✅ Yes' if has_h1 else '❌ No'}")

    # 3. Specific check for Prompts (JS vs Static)
    if 'prompt-library' in file_path.name:
        grid = soup.find(id='promptGrid')
        if grid and len(grid.get_text().strip()) == 0:
            print("   - ⚠️ WARNING: Prompt Grid is EMPTY in HTML source!")
            print("   - ℹ️ Google MUST execute JavaScript to see prompts on this page.")
        else:
            print("   - ✅ Prompts are pre-rendered in HTML.")
            
    # 4. Check data availability for JS
    if 'promptData' in content:
         print("   - ✅ 'promptData' variable found in source (Google can likely parse this).")

files = [
    'index.html',
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-veo-tech.html'
]

print("🤖 Google Bot Visibility Analysis")
print("================================")

for f in files:
    p = Path(f)
    if p.exists():
        simulate_google_bot(p)
    else:
        print(f"❌ File not found: {f}")

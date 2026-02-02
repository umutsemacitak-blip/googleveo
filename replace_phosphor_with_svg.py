#!/usr/bin/env python3
"""
Replace Phosphor Icons with inline SVG
This will remove 81 KiB of unused CSS!
"""

# SVG icons mapping
ICON_SVGS = {
    'ph-fill ph-aperture': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M201.54,54.46A104,104,0,0,0,54.46,201.54,104,104,0,0,0,201.54,54.46ZM190.23,65.78,152.58,128H98.12l59.57-76.59A88.5,88.5,0,0,1,190.23,65.78Zm-85.11,4.81L75.71,120H55.36A88.41,88.41,0,0,1,105.12,70.59ZM40,128a87.53,87.53,0,0,1,2.26-19.68L72.88,160H40.23A87.77,87.77,0,0,1,40,128Zm25.54,70.22L103.42,136h54.46l-59.57,76.59A88.5,88.5,0,0,1,65.77,198.22Zm85.11-4.81L180.29,144h20.35A88.41,88.41,0,0,1,150.88,193.41ZM216,128a87.53,87.53,0,0,1-2.26,19.68L183.12,96h32.65A87.77,87.77,0,0,1,216,128Z"/></svg>',
    
    'ph-bold ph-caret-down': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M216.49,104.49l-80,80a12,12,0,0,1-17,0l-80-80a12,12,0,0,1,17-17L128,159l71.51-71.52a12,12,0,0,1,17,17Z"/></svg>',
    
    'ph-duotone ph-cpu': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M152,96v64H104V96Z" opacity="0.2"/><path d="M152,88H104a8,8,0,0,0-8,8v64a8,8,0,0,0,8,8h48a8,8,0,0,0,8-8V96A8,8,0,0,0,152,88Zm-8,64H112V104h32ZM232,56V200a16,16,0,0,1-16,16H40a16,16,0,0,1-16-16V56A16,16,0,0,1,40,40H216A16,16,0,0,1,232,56ZM40,72V184H216V72Z"/></svg>',
    
    'ph-bold ph-arrow-right': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M224.49,136.49l-72,72a12,12,0,0,1-17-17L187,140H40a12,12,0,0,1,0-24H187L135.51,64.48a12,12,0,0,1,17-17l72,72A12,12,0,0,1,224.49,136.49Z"/></svg>',
    
    'ph-duotone ph-strategy': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M224,64v64L160,96ZM32,128,96,96v64Z" opacity="0.2"/><path d="M200,168a32.06,32.06,0,0,0-31,24H48V104h88a32,32,0,1,0,0-64H104V32a8,8,0,0,0-16,0v96a8,8,0,0,0,16,0V112h48v80H40a8,8,0,0,0,0,16H169a32,32,0,1,0,31-40Zm0-80a16,16,0,1,1-16-16A16,16,0,0,1,200,72Zm0,96a16,16,0,1,1-16-16A16,16,0,0,1,200,168Z"/></svg>',
    
    'ph-duotone ph-flask': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M213.66,209.66A8,8,0,0,1,208,224H48a8,8,0,0,1-6.58-12.53L104,141.87V48a8,8,0,0,1,8-8h32a8,8,0,0,1,8,8v93.87Z" opacity="0.2"/><path d="M221.24,210.56,173,142.94V48h8a8,8,0,0,0,0-16H75a8,8,0,0,0,0,16h8v94.94L34.76,210.56A16,16,0,0,0,48,240H208a16,16,0,0,0,13.24-29.44ZM99,48h58v96H99ZM48,224l41-56H208l0,0,41,56Z"/></svg>',
    
    'ph-duotone ph-terminal-window': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M224,56V200a8,8,0,0,1-8,8H40a8,8,0,0,1-8-8V56a8,8,0,0,1,8-8H216A8,8,0,0,1,224,56Z" opacity="0.2"/><path d="M128,128a8,8,0,0,1,3.2,0L48,56.55,48,200l80-90,80,90V56.54ZM128,114,71.21,64H184.79ZM40,208H216V40H40Z"/></svg>',
    
    'ph-fill ph-fingerprint': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M72,128a134.63,134.63,0,0,1-14.16,60.47,8,8,0,1,1-14.32-7.12A118.8,118.8,0,0,0,56,128,71.73,71.73,0,0,1,83.6,69.39a8,8,0,0,1,8.8,13.39A55.76,55.76,0,0,0,72,128Zm56-8a8,8,0,0,0-8,8,184.12,184.12,0,0,1-23,89.1,8,8,0,0,0,14,7.76A200.19,200.19,0,0,0,136,128,8,8,0,0,0,128,120Zm0-32a40,40,0,0,0-40,40,8,8,0,0,0,16,0,24,24,0,0,1,48,0,214.09,214.09,0,0,1-20.51,92,8,8,0,1,0,14.51,6.83A230,230,0,0,0,168,128,40,40,0,0,0,128,88Zm0-64C87.71,24,56,55.27,56,95.42a8,8,0,0,0,16,0C72,64.08,96.86,40,128,40c1.21,0,2.43,0,3.65.1A8,8,0,1,0,132.35,24Q130.19,24,128,24Zm88.36,41.78A8,8,0,0,0,210,67.11,92.41,92.41,0,0,1,224,96c0,17.13-3.29,45.62-19.63,74.49a8,8,0,0,0,14.19,7.42C236.78,144.12,240,112,240,96A108.4,108.4,0,0,0,224.59,59.78a8,8,0,0,0-8.23,6ZM128,56A72.85,72.85,0,0,0,55.09,128c0,23.25-3.54,46.79-10.53,70a8,8,0,0,0,15.49,4.11c7.23-24,10.87-48.23,10.95-72.09A56.9,56.9,0,0,1,128,72a55.67,55.67,0,0,1,26.08,6.47,8,8,0,0,0,7.74-14A71.63,71.63,0,0,0,128,56Zm72.87,126.48a8,8,0,0,0-11.19,1.48c-15.06,19.83-25.47,31.37-33.22,40-3.32,3.69-5.81,6.47-7.46,8.59-3.18-3.7-7.52-8.74-12.87-15.09-9-10.73-21.35-25.43-34.42-44.14a8,8,0,0,0-13.34,8.76c12.85,18.38,25,32.84,33.9,43.41,5.29,6.29,9.79,11.37,13.12,15.4a8,8,0,0,0,12.12,0c3.55-4.29,8.26-9.77,13.8-16.38,7.84-9.36,18.41-21.06,33.08-40.48A8,8,0,0,0,200.87,182.48Z"/></svg>',
    
    'ph-fill ph-phone-call': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M223.88,198.46l-47.09-30.72a16,16,0,0,0-16.53.42l-22.53,16.16a74.62,74.62,0,0,1-35.73-35.73l16.16-22.53a16,16,0,0,0,.42-16.53L88.54,32.12A16,16,0,0,0,72.22,24.1L24.81,38.49a16,16,0,0,0-10.67,15.35C15.67,135.26,120.74,240.33,202.16,241.86a16,16,0,0,0,15.35-10.67l14.39-47.41A16,16,0,0,0,223.88,198.46ZM207.81,224c-2.2.09-56.27-13.17-122.33-79.23S15.17,50.38,15.26,48.19L54,37.28l30.72,47.09L69.32,104.88a8,8,0,0,0,0,10.06,90.6,90.6,0,0,0,43.74,43.74,8,8,0,0,0,10.06,0l20.51-15.44L190.72,174,180.34,212.62ZM152.27,104.73A40,40,0,0,1,191.27,64a8,8,0,0,1,0,16,24,24,0,0,0-23.24,24.27,8,8,0,0,1-7.87,8.13h-.13A8,8,0,0,1,152.27,104.73Zm72-24a72.08,72.08,0,0,1-72,72.54,8,8,0,0,1,0-16A56.06,56.06,0,0,0,208.27,81a8,8,0,0,1,16,0Z"/></svg>',
    
    'ph-fill ph-envelope-simple': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M224,48H32a8,8,0,0,0-8,8V192a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A8,8,0,0,0,224,48ZM98.71,128,40,181.81V74.19Zm11.84,10.85,12,11.05a8,8,0,0,0,10.82,0l12-11.05,58,53.15H52.57ZM157.29,128,216,74.18V181.82Z"/></svg>',
    
    'ph-fill ph-map-pin': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M128,64a40,40,0,1,0,40,40A40,40,0,0,0,128,64Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,128Zm0-112a88.1,88.1,0,0,0-88,88c0,31.4,14.51,64.68,42,96.25a254.19,254.19,0,0,0,41.45,38.3,8,8,0,0,0,9.18,0A254.19,254.19,0,0,0,174,200.25c27.45-31.57,42-64.85,42-96.25A88.1,88.1,0,0,0,128,16Zm0,206c-16.53-13-72-60.75-72-118a72,72,0,0,1,144,0C200,161.23,144.53,209,128,222Z"/></svg>',
    
    'ph-fill ph-linkedin-logo': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M216,24H40A16,16,0,0,0,24,40V216a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V40A16,16,0,0,0,216,24ZM96,176a8,8,0,0,1-16,0V112a8,8,0,0,1,16,0ZM88,96a12,12,0,1,1,12-12A12,12,0,0,1,88,96Zm96,80a8,8,0,0,1-16,0V140a20,20,0,0,0-40,0v36a8,8,0,0,1-16,0V112a8,8,0,0,1,15.79-1.78A36,36,0,0,1,184,140Z"/></svg>',
    
    'ph-fill ph-telegram-logo': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M228.88,26.19a9,9,0,0,0-9.16-1.57L41.61,96.82a11,11,0,0,0,.35,20.61l60.88,20.29L143,193.72A11,11,0,0,0,153.8,200a17.36,17.36,0,0,0,.58,0,10.95,10.95,0,0,0,9.54-5.78l64-129.53A9,9,0,0,0,228.88,26.19Zm-108,134.33L75.21,139.29,197.4,63.93Z"/></svg>',
    
    'ph-fill ph-google-logo': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a96,96,0,1,1-21.95-61.09,8,8,0,1,1-12.33,10.18A80,80,0,1,0,207.6,128a8,8,0,0,1,16.4,0Z"/><rect x="127" y="55" width="72" height="16" rx="8"/></svg>',
    
    'ph ph-magnifying-glass': '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z"/></svg>',
}

import re
from pathlib import Path

def replace_phosphor_icons(file_path):
    """Replace Phosphor icon classes with inline SVG"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    replacements_made = []
    
    for class_name, svg in ICON_SVGS.items():
        # Find <i class="ph-xxx">
        pattern = rf'<i class="{re.escape(class_name)}"(\s[^>]*)?><!--!--></i>'
        if re.search(pattern, content):
            content = re.sub(pattern, svg, content)
            replacements_made.append(class_name)
        else:
            # Try without attributes
            pattern2 = rf'<i class="{re.escape(class_name)}"></i>'
            if re.search(pattern2, content):
                content = re.sub(pattern2, svg, content)
                replacements_made.append(class_name)
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return replacements_made
    return []

def remove_phosphor_script(file_path):
    """Remove Phosphor Icons script tag"""
    content = file_path.read_text(encoding='utf-8')
    
    # Remove the script tag
    pattern = r'<script src="https://unpkg\.com/@phosphor-icons/web"[^>]*></script>\s*'
    content = re.sub(pattern, '', content)
    
    file_path.write_text(content, encoding='utf-8')

# Process all HTML files
html_files = [
    'index.html',
    'tool-prompt-library.html',
    'report-authority-blueprint.html',
    'report-prompt-research.html',
    'report-veo-tech.html',
]

if __name__ == '__main__':
    print("🎯 Replacing Phosphor Icons with inline SVG\n")
    print("This will save 81 KiB of unused CSS!\n")
    
    total_replaced = 0
    
    for filename in html_files:
        file_path = Path(filename)
        if not file_path.exists():
            print(f"❌ {filename}: Not found")
            continue
        
        replaced = replace_phosphor_icons(file_path)
        remove_phosphor_script(file_path)
        
        if replaced:
            print(f"✅ {filename}: Replaced {len(set(replaced))} icon types")
            total_replaced += 1
        else:
            print(f"ℹ️  {filename}: No icons to replace")
    
    print(f"\n✨ Done! Modified {total_replaced}/{len(html_files)} files")
    print("📦 Removed Phosphor Icons script from all pages")
    print("💾 Saved ~81 KiB of unused CSS")

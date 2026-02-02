import re

file_path = 'data.js'
content = open(file_path, 'r', encoding='utf-8').read()

replacements = {
    '"Aşamalı Metamorfoz"': '"Progressive Metamorphosis"',
    '"Antik Zanaatların Sinematik Detayları"': '"Ancient Cinematic Crafts"',
    '"Sıvı Dinamikleri ve Ferrofluid Sanatı"': '"Fluid Dynamics & Ferrofluid Art"',
    '"Biyolüminesanslı Derin Deniz Keşfi"': '"Bioluminescent Deep Sea Exploration"',
    '"Mikroskobik Dünyalar"': '"Microscopic Worlds"',
    '"Mimari Ütopyalar"': '"Architectural Utopias"',
    '"Siberpunk Sokak Lezzetleri"': '"Cyberpunk Street Food"',
    '"Mekanik Böcekler"': '"Mechanical Insects"',
    '"Portrelerde Duygu Analizi"': '"Emotional Analysis in Portraits"',
    '"Soyut Veri Akışları"': '"Abstract Data Streams"'
}

# Be careful to only replace keys, i.e., followed by : [
# The regex ensures we match "Key": [
for turk, eng in replacements.items():
    pattern = re.escape(turk) + r'\s*:\s*\['
    replacement = eng + ': ['
    
    # Check if exists
    if re.search(pattern, content):
        print(f"Found and replacing: {turk} -> {eng}")
        content = re.sub(pattern, replacement, content)
    else:
        print(f"Not found as key: {turk}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Translation complete.")

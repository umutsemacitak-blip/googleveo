
import re

def scope_css(css_content, scope_id):
    # Extract @imports first
    imports = []
    import_lines = re.findall(r'@import.*?;', css_content)
    for imp in import_lines:
        imports.append(imp)
        css_content = css_content.replace(imp, "")

    # Clean up and split
    lines = css_content.split('}')
    scoped_lines = []
    
    for line in lines:
        if '{' in line:
            parts = line.split('{')
            selector_part = parts[0]
            body_part = parts[1]
            
            # Split multiple selectors by comma
            selectors = selector_part.split(',')
            scoped_selectors = []
            for s in selectors:
                s = s.strip()
                if not s: continue
                # Do not scope keyframes or font-face if present (basic check)
                if s.startswith('@'):
                     scoped_selectors.append(s)
                else:
                     scoped_selectors.append(f"#{scope_id} {s}")
            
            if scoped_selectors:
                new_line = ", ".join(scoped_selectors) + " {" + body_part + "}"
                scoped_lines.append(new_line)
        else:
            if line.strip():
                scoped_lines.append(line)
                
    return "\n".join(imports), "\n".join(scoped_lines)

def process_file(source_file, target_file, title, scope_id, next_prev_links=None):
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Style
    style_match = re.search(r'<style type="text/css">(.*?)</style>', content, re.DOTALL)
    if not style_match:
        # Try without type attr
        style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    
    css_content = style_match.group(1) if style_match else ""
    # Scope the CSS
    css_imports, scoped_css = scope_css(css_content, scope_id)

    # Extract Body Content
    # We want strictly what's inside <body ...> ... </body>
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    body_content = body_match.group(1) if body_match else "Content not found."

    # Build New HTML with Antigravity Layout
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta name="description" content="{title} - BQ5M Intelligence Report">
    <title>{title} | BQ5M Intelligence</title>
    
    <!-- Preconnect -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="style.css">
    <script src="https://unpkg.com/@phosphor-icons/web" defer></script>
    <style>
        /* External Imports */
        {css_imports}

        /* Scoped Google Docs Styles */
        {scoped_css}
        
        /* Overrides to make text readable on dark background if necessary */
        #{scope_id} p, #{scope_id} span, #{scope_id} h1, #{scope_id} h2, #{scope_id} h3, #{scope_id} li {{
             /* Resets handled by specific overrides below */
        }}
        
        /* Force Text Color Override for Antigravity Look */
        #{scope_id} {{
            color: #e0e0e0 !important;
            padding: 2rem;
        }}
        #{scope_id} h1, #{scope_id} h2, #{scope_id} h3, #{scope_id} h4 {{
            color: var(--neon-cyan) !important;
        }}
        #{scope_id} span, #{scope_id} p, #{scope_id} li {{
            color: #d0d0d0 !important;
            background-color: transparent !important;
        }}
        #{scope_id} table td, #{scope_id} table th {{
            border-color: var(--glass-border) !important;
            background-color: rgba(255,255,255,0.02) !important;
        }}
        #{scope_id} a {{
            color: var(--neon-iris) !important;
        }}

        /* MOBILE OVERRIDES */
        @media (max-width: 900px) {{
            #{scope_id} [class*="c"] {{
               padding: 0 !important;
               max-width: 100% !important;
               width: 100% !important;
            }}
            #{scope_id} {{
                padding: 1rem !important;
            }}
            .article-body {{
                padding: 0 1rem;
            }}
            /* Fix for cutoff tables on mobile */
            #{scope_id} table {{
                display: block;
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <!-- NEURO-HEADER -->
        <header class="site-header">
            <a href="index.html" class="brand">
                <i class="ph-fill ph-aperture"></i>
                <span>BQ5M <span style="opacity:0.5; font-weight:300;">LABS</span></span>
            </a>
            <nav class="nav-links">
                <a href="index.html" class="nav-link">Intelligence</a>
                <a href="tool-prompt-library.html" class="nav-link">Prompt Nexus</a>
                <a href="#contact" class="nav-link">Contact</a>
            </nav>
        </header>

        <!-- MAIN CONTENT -->
        <main class="page-content" style="padding-top:120px;">
            <div class="article-container">
                <!-- Original Content Injected Here -->
                <div id="{scope_id}" class="article-body" style="max-width:900px; margin:0 auto;">
                    {body_content}
                </div>
            </div>

            <!-- CONTACT INTEGRATION (Floating Anchor - Consistent) -->
            <section id="contact" class="contact-anchor" style="margin-top:8rem;">
                <div class="glass-panel">
                    <div class="contact-info">
                        <h3>Communication Hub</h3>
                        
                        <div class="contact-list">
                            <div class="contact-item">
                                <div class="c-icon"><i class="ph-fill ph-fingerprint"></i></div>
                                <div class="c-detail">
                                    <span class="c-label">Identity</span>
                                    <span class="c-value">Umut Çıtak</span>
                                </div>
                            </div>
                            <a href="tel:+905404374371" class="contact-item">
                                <div class="c-icon" style="color:var(--neon-iris)"><i class="ph-fill ph-phone-call"></i></div>
                                <div class="c-detail">
                                    <span class="c-label">Secure Line</span>
                                    <span class="c-value">+90 540 437 437 1</span>
                                </div>
                            </a>
                            <a href="mailto:info@bq5m.com" class="contact-item">
                                <div class="c-icon"><i class="ph-fill ph-envelope-simple"></i></div>
                                <div class="c-detail">
                                    <span class="c-label">Digital Relay</span>
                                    <span class="c-value">info@bq5m.com</span>
                                </div>
                            </a>
                            <div class="contact-item">
                                <div class="c-icon"><i class="ph-fill ph-map-pin"></i></div>
                                <div class="c-detail">
                                    <span class="c-label">Physical Coordinates</span>
                                    <span class="c-value">Çukurambar Next Level 105/A34-7165<br>Ankara, TR</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>
    <script src="script.js" defer></script>
</body>
</html>
"""
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Processed {target_file}")

# Execute
try:
    process_file("10PhaseAuthorityBlueprintMasteringGoogleVeo3i.html", "report-authority-blueprint.html", "10-Phase Authority Blueprint", "google-report-1")
    process_file("GoogleVeo3SEOMakaleretimi.html", "report-veo-tech.html", "Technical Analysis: Veo 3", "google-report-2")
    process_file("GoogleVeoPromptEngineeringResearch.html", "report-prompt-research.html", "Veo 3 Prompt Engineering Research", "google-report-3")
except Exception as e:
    print(f"Error: {e}")

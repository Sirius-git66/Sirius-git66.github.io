"""Fix the corrupted CSS in commodities_dashboard.py"""

# Read the file
with open(r"C:\Users\being\OneDrive\Documents\Projects\Web Scrape\commodities_dashboard.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the corrupted CSS (the one with literal \n)
corrupted_pattern = r'}}`n        `n        /\* Educational Guide Section \*/.*?`n        `n        /\* Forward Curves Section \*/'

# Replace with clean CSS
clean_css = '''}}
        
        /* Educational Guide Section */
        .guide-section {{
            background: #111111;
            border-radius: 4px;
            padding: 16px;
            border: 1px solid #1a1a1a;
            text-align: center;
        }}
        
        .guide-link {{
            display: block;
            text-decoration: none;
            color: inherit;
        }}
        
        .guide-icon-container {{
            margin: 10px auto 0 auto;
            display: inline-block;
            padding: 12px;
            border-radius: 4px;
            border: 1px solid transparent;
            transition: all 0.5s ease-out;
            animation: gentle-pulse 3s ease-in-out infinite;
            position: relative;
            transform-origin: center center;
        }}
        
        @keyframes gentle-pulse {{
            0%, 100% {{ box-shadow: 0 0 0 rgba(0, 212, 255, 0); }}
            50% {{ box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }}
        }}
        
        .guide-icon-container:hover {{
            border-color: #00d4ff;
            transform: scale(4.5);
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
            z-index: 100;
        }}
        
        .guide-icon {{
            max-width: 70px;
            height: auto;
            display: block;
        }}
        
        .guide-text {{
            font-size: 0.85em;
            font-weight: 600;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 14px;
            padding-bottom: 8px;
            border-bottom: 1px solid #1a1a1a;
            transition: color 0.3s ease;
        }}
        
        .guide-section:hover .guide-text {{
            color: #00d4ff;
        }}
        
        /* News and Guide Grid */
        .bottom-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 12px;
        }}
        
        @media (max-width: 1100px) {{
            .bottom-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* Forward Curves Section */'''

# Use regex to replace
import re
content = re.sub(corrupted_pattern, clean_css, content, flags=re.DOTALL)

# Write back
with open(r"C:\Users\being\OneDrive\Documents\Projects\Web Scrape\commodities_dashboard.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ commodities_dashboard.py CSS fixed!")

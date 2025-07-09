#!/usr/bin/env python3
import os
import re

def create_chapter_html(chapter_num, chapter_title, content, total_chapters=24):
    """Generate HTML for a single chapter"""
    
    # Process content to add paragraph tags and handle part dividers
    lines = content.split('\n')
    processed_content = []
    in_paragraph = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_paragraph:
                processed_content.append('</p>')
                in_paragraph = False
            continue
            
        # Check if this is a part divider
        if line.startswith('Part ') and ':' in line:
            if in_paragraph:
                processed_content.append('</p>')
                in_paragraph = False
            processed_content.append(f'<div class="part-divider">{line}</div>')
        else:
            if not in_paragraph:
                processed_content.append('<p>')
                in_paragraph = True
            processed_content.append(line)
    
    if in_paragraph:
        processed_content.append('</p>')
    
    # Navigation logic
    prev_link = f'chapter{chapter_num-1}.html' if chapter_num > 1 else 'index.html'
    prev_text = f'Chapter {chapter_num-1}' if chapter_num > 1 else 'Cover'
    next_link = f'chapter{chapter_num+1}.html' if chapter_num < total_chapters else ''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter {chapter_num}: {chapter_title} - Scout's Haven</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="chapter-container">
        <div class="chapter-header">
            <div class="chapter-number">Chapter {chapter_num}</div>
            <h1 class="chapter-title">{chapter_title}</h1>
        </div>
        
        <div class="chapter-content">
            {'\n            '.join(processed_content)}
        </div>
        
        <div class="navigation">
            <a href="{prev_link}" class="nav-button">← Previous: {prev_text}</a>
            <a href="index.html" class="nav-home">Table of Contents</a>
            {'<a href="' + next_link + '" class="nav-button">Next: Chapter ' + str(chapter_num+1) + ' →</a>' if next_link else '<span class="nav-button disabled">The End</span>'}
        </div>
    </div>
</body>
</html>'''
    
    return html

# Chapter titles mapping
chapter_titles = {
    1: "Dawn at Big Verde",
    2: "Fracture", 
    3: "Hot Foot Chaos",
    4: "Patchwork Trials",
    5: "Patchwork Place",
    6: "The Cracking Roof",
    7: "Define the Quest",
    8: "Ironwood Illusion",
    9: "Canyon Furnace",
    10: "Midden Dead-Ends",
    11: "Far-Bosque Idea",
    12: "Into the Arroyo",
    13: "Ridge of Mirrors",
    14: "First Setback Night",
    15: "Storm over the Plain",
    16: "Bosque Revelation",
    17: "Measuring the Trees",
    18: "Choice of Hollow",
    19: "Dust-Storm Trial",
    20: "Community Call",
    21: "Distributed Design",
    22: "Flash-Flood Finale",
    23: "Naming Scout's Haven",
    24: "Starlight Epilogue"
}

# Process each chapter file
for i in range(1, 25):
    # Construct filename
    filename = f"Chapter_{i:02d}_{chapter_titles[i].replace(' ', '_')}.txt"
    
    # Check for alternate naming patterns
    if not os.path.exists(filename):
        # Try with "Scouts" instead of "Scout's"
        alt_filename = filename.replace("Scout's", "Scouts")
        if os.path.exists(alt_filename):
            filename = alt_filename
    
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove the chapter title from the content (first line)
        lines = content.split('\n')
        if lines[0].startswith(f'Chapter {i}:'):
            content = '\n'.join(lines[1:])
        
        # Generate HTML
        html_content = create_chapter_html(i, chapter_titles[i], content)
        
        # Write HTML file
        with open(f'chapter{i}.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Generated chapter{i}.html - {chapter_titles[i]}")
    else:
        print(f"Warning: Could not find {filename}")

print("\nAll chapters generated successfully!")
print("\nTo publish your book:")
print("1. Push all files to GitHub")
print("2. Go to Settings > Pages in your repository")
print("3. Under 'Source', select 'Deploy from a branch'")
print("4. Choose 'main' branch and '/ (root)' folder")
print("5. Click Save")
print("6. Your book will be available at: https://[your-username].github.io/Shade-Book/")
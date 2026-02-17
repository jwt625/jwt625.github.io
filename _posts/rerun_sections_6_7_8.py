#!/usr/bin/env python3
"""Re-run sections 6, 7, and 8 of the scraping script."""

import os
import re
import shutil
import json
from datetime import datetime
from helpers_LLM import process_with_llm_from_files

# Find the latest OFS file
import glob
ofs_files = glob.glob("*-weekly-OFS-*.md")
ofs_files = [f for f in ofs_files if not f.startswith('trash_')]
ofs_files.sort()
output_md_file = ofs_files[-1]
print(f"Using OFS file: {output_md_file}")

print("\n" + "="*60)
print("SECTION 6: EXTRACTING TAGS AND SECTION TITLES USING LLM")
print("="*60)

output_file = f"output_{datetime.now().strftime('%Y%m%d')}.md"
res = process_with_llm_from_files(config_file='config.json',
                                  prompt_file='prompt_extract_tag_section.md',
                                  content_file=output_md_file,
                                  output_file=output_file)
print(f"LLM processing completed. Output saved to: {output_file}")

print("\n" + "="*60)
print("SECTION 7: PROCESSING MARKDOWN FILES")
print("="*60)

def process_markdown_files(header_file, output_file, content_file):
    # 1. Read the header template
    with open(header_file, 'r', encoding='utf-8') as f:
        header_content = f.read()
    
    # 2. Extract tags from the first markdown codeblock in output.md
    with open(output_file, 'r', encoding='utf-8') as f:
        output_content = f.read()
    
    # Find the first markdown codeblock with tags
    tags_match = re.search(r'```markdown\n(.*?)\n```', output_content, re.DOTALL)
    if not tags_match:
        raise Exception("Could not find tags in the output file")
    
    tags_content = tags_match.group(1).strip()
    
    # 3. Add the extracted tags below the 'tags:' in the header
    tags_pos = header_content.find('tags:')
    if tags_pos == -1:
        raise Exception("Could not find 'tags:' in the header template")
    
    new_header = header_content[:tags_pos + 5] + '\n' + tags_content + header_content[tags_pos + 5:]
    
    # 5. Extract section titles from the second markdown codeblock
    titles_match = re.search(r'```markdown\n(.*?)\n```', output_content[tags_match.end():], re.DOTALL)
    if not titles_match:
        raise Exception("Could not find section titles in the output file")
    
    titles_content = titles_match.group(1).strip()
    
    # Parse the titles into a list
    section_titles = []
    for line in titles_content.split('\n'):
        if line.startswith('#'):
            title = line[1:].strip()
            section_titles.append(title)
    
    # 4. Read the content file
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 6. Locate corresponding sections by numerical indices
    section_pattern = r'^(\d+)\.\s+(.*?)$'
    section_matches = list(re.finditer(section_pattern, content, re.MULTILINE))
    
    # Create a mapping of section numbers to titles
    section_number_to_title = {}
    
    for i, match in enumerate(section_matches):
        section_number = match.group(1)
        section_text = match.group(2)
        
        if i < len(section_titles):
            section_number_to_title[section_number] = section_titles[i]
        else:
            section_number_to_title[section_number] = section_text
    
    # 7. Remove numerical indices and insert extracted section titles
    new_content = content
    for section_number, title in section_number_to_title.items():
        pattern = f'^{section_number}\\.\\s+'
        replacement = f'# {title}\n\n'
        new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)
    
    final_content = new_header + '\n\n' + new_content
    
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Successfully processed markdown files and updated {content_file}")

process_markdown_files('standard_header.md', output_file, output_md_file)

print("\n" + "="*60)
print("SECTION 8: CLEANING UP FILES")
print("="*60)

scraping_folder = 'scraping'
os.makedirs(scraping_folder, exist_ok=True)

posts_dir = '.'
for filename in os.listdir(posts_dir):
    if filename.startswith(('output_', 'scraped_', 'sorted_')):
        source_path = os.path.join(posts_dir, filename)
        dest_path = os.path.join(scraping_folder, filename)
        shutil.move(source_path, dest_path)
        print(f"Moved {filename} to {scraping_folder}")

print("\n" + "="*60)
print("SCRIPT COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"Final blog post: {output_md_file}")


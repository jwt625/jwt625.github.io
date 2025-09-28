#!/usr/bin/env python3
"""
Google Docs Batch Import Pipeline for Jekyll Blog
Converts HTML zip exports to Jekyll markdown posts with proper image handling.
"""

import os
import sys
import zipfile
import shutil
import argparse
import yaml
import re
import subprocess
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from slugify import slugify

class GoogleDocsImporter:
    def __init__(self, blog_root, dry_run=False):
        self.blog_root = Path(blog_root)
        self.dry_run = dry_run
        self.manifest_file = self.blog_root / '.import-manifest.yaml'
        self.temp_dir = Path('/tmp/gdocs-import')
        
        # Ensure directories exist
        self.posts_dir = self.blog_root / '_posts'
        self.assets_dir = self.blog_root / 'assets' / 'images' / 'imported'
        
        if not self.dry_run:
            self.assets_dir.mkdir(parents=True, exist_ok=True)
            self.temp_dir.mkdir(exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Log with dry-run prefix if applicable"""
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}{level}: {message}")
    
    def generate_slug(self, zip_path):
        """Generate URL-safe slug from zip filename"""
        filename = Path(zip_path).stem
        # Remove date prefixes and clean up
        cleaned = re.sub(r'^\d{8}\s*-\s*', '', filename)  # Remove "20190903 - "
        cleaned = re.sub(r'^WJ\s*-\s*', '', cleaned)      # Remove "WJ - "
        return slugify(cleaned)
    
    def extract_zip(self, zip_path):
        """Extract zip file to temporary directory"""
        zip_name = Path(zip_path).stem
        extract_dir = self.temp_dir / zip_name

        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        self.log(f"Extracting {zip_path} to {extract_dir}")

        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        return extract_dir
    
    def find_html_file(self, extract_dir):
        """Find the main HTML file in extracted directory"""
        html_files = list(extract_dir.glob('*.html'))
        if not html_files:
            raise ValueError(f"No HTML file found in {extract_dir}")
        if len(html_files) > 1:
            self.log(f"Multiple HTML files found, using first: {html_files[0]}")
        return html_files[0]
    
    def copy_images(self, extract_dir, doc_slug):
        """Copy images to Jekyll assets directory"""
        images_src = extract_dir / 'images'
        if not images_src.exists():
            self.log(f"No images directory found in {extract_dir}")
            return []
        
        images_dest = self.assets_dir / doc_slug
        copied_images = []
        
        self.log(f"Copying images from {images_src} to {images_dest}")
        
        if not self.dry_run:
            images_dest.mkdir(parents=True, exist_ok=True)
            
            for img_file in images_src.glob('*'):
                if img_file.is_file():
                    dest_file = images_dest / img_file.name
                    shutil.copy2(img_file, dest_file)
                    copied_images.append(str(dest_file.relative_to(self.blog_root)))
        else:
            # For dry-run, simulate the file list
            for img_file in images_src.glob('*'):
                if img_file.is_file():
                    copied_images.append(f"assets/images/imported/{doc_slug}/{img_file.name}")
        
        self.log(f"Copied {len(copied_images)} images")
        return copied_images
    
    def fix_image_paths(self, html_content, doc_slug):
        """Fix image paths in HTML before pandoc conversion"""
        self.log("Fixing image paths in HTML")

        # Replace relative image paths with Jekyll asset paths
        fixed_html = re.sub(
            r'src="images/([^"]+)"',
            f'src="/assets/images/imported/{doc_slug}/\\1"',
            html_content
        )

        # Also handle src='images/...' (single quotes)
        fixed_html = re.sub(
            r"src='images/([^']+)'",
            f"src='/assets/images/imported/{doc_slug}/\\1'",
            fixed_html
        )

        return fixed_html

    def clean_google_docs_html(self, html_content):
        """Clean up Google Docs specific HTML artifacts"""
        self.log("Cleaning Google Docs HTML artifacts")

        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove Google Docs style elements
        for style_tag in soup.find_all('style'):
            style_tag.decompose()

        # Remove all style attributes from all elements
        for element in soup.find_all(attrs={"style": True}):
            del element['style']

        # Remove or clean up spans with Google Docs classes
        for span in soup.find_all('span'):
            # Remove class attributes that start with 'c' followed by numbers
            if span.get('class'):
                classes = span.get('class', [])
                # Remove Google Docs classes like 'c3', 'c15', etc.
                cleaned_classes = [cls for cls in classes if not re.match(r'^c\d+$', cls)]
                if cleaned_classes:
                    span['class'] = cleaned_classes
                else:
                    # Remove class attribute entirely if no valid classes remain
                    del span['class']

            # If span has no attributes left, unwrap it
            if not span.attrs:
                span.unwrap()

        # Clean up image tags - remove complex styling
        for img in soup.find_all('img'):
            # Keep only essential attributes
            essential_attrs = {}
            if img.get('src'):
                essential_attrs['src'] = img['src']
            if img.get('alt'):
                essential_attrs['alt'] = img['alt']

            # Clear all attributes and set only essential ones
            img.attrs.clear()
            img.attrs.update(essential_attrs)

        # Clean up malformed links with Google redirect URLs
        for link in soup.find_all('a'):
            href = link.get('href', '')
            # Fix Google redirect URLs
            if 'google.com/url?q=' in href:
                # Extract the actual URL from Google redirect
                import urllib.parse
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if 'q' in parsed:
                    actual_url = parsed['q'][0]
                    link['href'] = actual_url

            # Remove unnecessary attributes
            attrs_to_keep = ['href', 'title']
            for attr in list(link.attrs.keys()):
                if attr not in attrs_to_keep:
                    del link[attr]

        # Remove empty paragraphs and divs
        for tag in soup.find_all(['p', 'div']):
            if not tag.get_text(strip=True) and not tag.find_all(['img', 'br']):
                tag.decompose()

        # Clean up links with Google Docs artifacts
        for link in soup.find_all('a'):
            # Remove Google Docs classes
            if link.get('class'):
                classes = link.get('class', [])
                cleaned_classes = [cls for cls in classes if not re.match(r'^c\d+$', cls)]
                if cleaned_classes:
                    link['class'] = cleaned_classes
                else:
                    del link['class']

        return str(soup)
    
    def extract_metadata(self, html_content, zip_path):
        """Extract metadata from HTML for front matter"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract title - prefer Google Docs title class over standard headings
        title = None

        # First try to find Google Docs title (p.title or p.c*title)
        title_element = soup.find('p', class_=lambda x: x and ('title' in x or any('title' in cls for cls in x)))
        if not title_element:
            # Also try looking for elements with id containing title-like patterns
            title_element = soup.find('p', id=lambda x: x and 'title' in x.lower())

        if title_element:
            title_text = title_element.get_text().strip()
            # Clean up Google Docs artifacts from title
            title_text = re.sub(r'\{[^}]*\}', '', title_text)  # Remove {.class}
            title_text = re.sub(r'^\[([^\]]+)\]$', r'\1', title_text)  # Remove [brackets]
            if title_text and len(title_text) > 3:  # Meaningful title
                title = title_text

        # If no title class found, try standard headings
        if not title:
            for heading_tag in ['h1', 'h2', 'h3']:
                heading = soup.find(heading_tag)
                if heading:
                    title_text = heading.get_text().strip()
                    # Clean up Google Docs artifacts from title
                    title_text = re.sub(r'\{[^}]*\}', '', title_text)  # Remove {.class}
                    title_text = re.sub(r'^\[([^\]]+)\]$', r'\1', title_text)  # Remove [brackets]
                    if title_text and len(title_text) > 3:  # Meaningful title
                        title = title_text
                        break

        # If no good heading found, try first paragraph with substantial text
        if not title:
            paragraphs = soup.find_all('p')
            for p in paragraphs[:3]:  # Check first 3 paragraphs
                text = p.get_text().strip()
                # Clean up artifacts
                text = re.sub(r'\{[^}]*\}', '', text)
                text = re.sub(r'^\[([^\]]+)\]$', r'\1', text)
                # Skip author/date lines
                if text and len(text) > 10 and not re.match(r'^(Wentao Jiang|WJ)', text):
                    title = text[:100]  # Truncate if too long
                    break

        # Final fallback to cleaned filename
        if not title:
            title = Path(zip_path).stem
            title = re.sub(r'^WJ\s*-\s*', '', title)  # Remove "WJ - " prefix
            title = re.sub(r'^\d{8}\s*-\s*', '', title)  # Remove date prefix
        
        # Extract author and date from content
        author = "Wentao Jiang"  # Default
        original_date = None
        
        # Look for date patterns in first few paragraphs
        first_paragraphs = soup.find_all('p')[:5]
        for p in first_paragraphs:
            text = p.get_text()
            # Look for patterns like "Wentao Jiang, 20180428"
            date_match = re.search(r'(\d{8})', text)
            if date_match:
                date_str = date_match.group(1)
                try:
                    original_date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
                except ValueError:
                    pass
        
        # Auto-categorize based on content/filename
        categories = ["Research"]  # Default
        tags = []
        
        # Simple keyword-based tagging
        content_lower = html_content.lower()
        if 'lithium niobate' in content_lower or 'lnx' in content_lower:
            tags.extend(["Lithium Niobate", "Materials"])
        if 'piezoelectric' in content_lower:
            tags.append("Piezoelectric")
        if 'simulation' in content_lower or 'comsol' in content_lower:
            tags.append("Simulation")
        if 'properties' in content_lower:
            tags.append("Reference")
        
        return {
            'title': title,
            'author': author,
            'original_date': original_date,
            'categories': categories,
            'tags': tags if tags else ["Technical"]
        }
    
    def convert_to_markdown(self, html_content):
        """Convert HTML to markdown using pandoc"""
        self.log("Converting HTML to markdown with pandoc")

        if self.dry_run:
            return "# [DRY-RUN] Markdown content would be generated here\n\nOriginal HTML would be converted..."

        try:
            # Write HTML to temp file
            temp_html = self.temp_dir / 'temp.html'
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Run pandoc with better options for Google Docs content
            result = subprocess.run([
                'pandoc',
                str(temp_html),
                '-f', 'html',
                '-t', 'markdown',
                '--wrap=none',
                '--strip-comments'
            ], capture_output=True, text=True, encoding='utf-8')

            if result.returncode != 0:
                raise RuntimeError(f"Pandoc failed: {result.stderr}")

            # Clean up the converted markdown
            cleaned_markdown = self.clean_converted_markdown(result.stdout)

            # Escape Liquid syntax before returning
            return self.escape_liquid_syntax(cleaned_markdown)

        except FileNotFoundError:
            raise RuntimeError("Pandoc not found. Please install pandoc: brew install pandoc")

    def escape_liquid_syntax(self, markdown_content):
        """Escape Liquid template syntax in markdown content"""
        import re

        # Simple approach: escape all {{ }} patterns
        # Replace {{ with \{\{ and }} with \}\}
        escaped_content = markdown_content.replace('{{', '\\{\\{').replace('}}', '\\}\\}')

        self.log(f"Escaped {markdown_content.count('{{')} Liquid syntax patterns")

        return escaped_content

    def clean_converted_markdown(self, markdown_content):
        """Clean up markdown content after pandoc conversion"""
        self.log("Cleaning converted markdown")

        # Remove Google Docs CSS class artifacts that might remain
        # Pattern: {.c3}, {.c15 .c9}, etc.
        cleaned = re.sub(r'\{\.c\d+[^}]*\}', '', markdown_content)

        # Remove empty span artifacts: [text]{.class} -> text
        cleaned = re.sub(r'\[([^\]]+)\]\{[^}]*\}', r'\1', cleaned)

        # Remove square brackets around normal text (Google Docs artifact)
        # But preserve markdown links [text](url) and images ![alt](url)
        # Pattern: [text] that is NOT followed by ( or preceded by !
        cleaned = re.sub(r'(?<!\!)(?<!\[)\[([^\]]+)\](?!\()', r'\1', cleaned)

        # Clean up image markdown and add auto alt text
        def clean_image_markdown(match):
            alt_text = match.group(1).strip()
            image_url = match.group(2)

            # If alt text is empty, generate from image filename
            if not alt_text:
                # Extract filename from path like /assets/images/imported/doc/image123.png
                filename = image_url.split('/')[-1]
                # Remove extension and create readable alt text
                alt_text = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '').replace('image', 'Image ')

            return f'![{alt_text}]({image_url})'

        # Clean up images with style attributes
        cleaned = re.sub(
            r'!\[([^\]]*)\]\(([^)]+)\)\{[^}]*\}',
            clean_image_markdown,
            cleaned
        )

        # Clean up regular images with empty alt text (no style attributes)
        cleaned = re.sub(
            r'!\[([^\]]*)\]\(([^)]+)\)',
            clean_image_markdown,
            cleaned
        )

        # Split multiple images on the same line into separate lines first
        # Handle consecutive images like ![img1](path1)![img2](path2)
        consecutive_images_pattern = r'(!\[[^\]]*\]\([^)]+\))(!\[[^\]]*\]\([^)]+\))'

        # Keep splitting until no more consecutive images found
        max_iterations = 10
        iteration = 0

        while re.search(consecutive_images_pattern, cleaned) and iteration < max_iterations:
            cleaned = re.sub(consecutive_images_pattern, r'\1\n\2', cleaned)
            iteration += 1

        # Debug: log if we had to split images
        if iteration > 0:
            self.log(f"Split {iteration} sets of consecutive images")

        # Remove standalone CSS class references
        cleaned = re.sub(r'^\{\.c\d+[^}]*\}\s*$', '', cleaned, flags=re.MULTILINE)

        # Clean up table of contents links with Google Docs anchors
        # Convert: [[Text](#h.abc123){.c6}] to: [Text](#text)
        def clean_toc_link(match):
            text = match.group(1)
            # Generate a simple anchor from the text
            anchor = re.sub(r'[^\w\s-]', '', text.lower())
            anchor = re.sub(r'\s+', '-', anchor.strip())
            return f'[{text}](#{anchor})'

        cleaned = re.sub(
            r'\[\[([^\]]+)\]\(#[^)]+\)\{[^}]*\}\]',
            clean_toc_link,
            cleaned
        )

        # Fix escaped characters that shouldn't be escaped
        # Remove unnecessary backslashes before apostrophes and other characters
        cleaned = re.sub(r"\\(')", r"\1", cleaned)  # Fix \' -> '
        cleaned = re.sub(r"\\(\*)", r"\1", cleaned)  # Fix \* -> *
        cleaned = re.sub(r"\\(\+)", r"\1", cleaned)  # Fix \+ -> +
        cleaned = re.sub(r"\\(\?)", r"\1", cleaned)  # Fix \? -> ?
        cleaned = re.sub(r"\\(\|)", r"\1", cleaned)  # Fix \| -> |
        cleaned = re.sub(r"\\(\()", r"\1", cleaned)  # Fix \( -> (
        cleaned = re.sub(r"\\(\))", r"\1", cleaned)  # Fix \) -> )
        cleaned = re.sub(r"\\(\[)", r"\1", cleaned)  # Fix \[ -> [
        cleaned = re.sub(r"\\(\])", r"\1", cleaned)  # Fix \] -> ]

        # Remove empty lines with just CSS classes
        cleaned = re.sub(r'^\s*\[?\]\{[^}]*\}\s*$', '', cleaned, flags=re.MULTILINE)

        # Clean up multiple consecutive empty lines
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)

        # Remove leading/trailing whitespace from lines
        lines = [line.rstrip() for line in cleaned.split('\n')]
        cleaned = '\n'.join(lines)

        # Remove any remaining empty CSS class artifacts
        cleaned = re.sub(r'\[\]\{[^}]*\}', '', cleaned)

        # Clean up empty divs and spans that remain
        cleaned = re.sub(r'::: \{\}\s*\[\]\{[^}]*\}\s*:::', '', cleaned)
        cleaned = re.sub(r'::: \{\}\s*\[\]\s*:::', '', cleaned)

        # Remove standalone empty brackets
        cleaned = re.sub(r'^\s*\[\]\s*$', '', cleaned, flags=re.MULTILINE)

        # Clean up malformed table of contents with Google Docs links
        def create_jekyll_anchor(text):
            """Convert heading text to Jekyll/Kramdown anchor format"""
            # Remove any existing brackets and clean up
            text = re.sub(r'[\[\]]', '', text)
            # Convert to lowercase, replace spaces and special chars with hyphens
            anchor = re.sub(r'[^\w\s-]', '', text.lower())
            anchor = re.sub(r'[-\s]+', '-', anchor)
            return anchor.strip('-')

        def fix_toc_link(match):
            text = match.group(1)
            anchor = create_jekyll_anchor(text)
            return f'[{text}](#{anchor})'

        # Pattern: [Text](#h.abc123)        [Number](#h.abc123)
        cleaned = re.sub(r'\[([^\]]+)\]\(#h\.[^)]+\)\s*\[[^\]]*\]\(#h\.[^)]+\)', fix_toc_link, cleaned)

        # Pattern: [[Text](#h.abc123)][        ][[Number](#h.abc123)]
        cleaned = re.sub(r'\[\[([^\]]+)\]\(#[^)]+\)\]\s*\[\s*\]\s*\[\[[^\]]*\]\(#[^)]+\)\]', fix_toc_link, cleaned)

        # Simplify remaining TOC patterns
        cleaned = re.sub(r'\[\[([^\]]+)\]\(#[^)]+\)\]', fix_toc_link, cleaned)

        # Fix simple Google Docs anchor links
        cleaned = re.sub(r'\[([^\]]+)\]\(#h\.[^)]+\)', fix_toc_link, cleaned)

        # Remove any remaining style attributes from any elements
        cleaned = re.sub(r'\{style="[^"]*"\}', '', cleaned)

        # Remove any remaining inline style attributes that might have been converted differently
        cleaned = re.sub(r'style="[^"]*"', '', cleaned)

        # Remove Google Docs heading anchor syntax: {#h.abc123 .c4}
        cleaned = re.sub(r'\{#[^}]*\}', '', cleaned)

        # Fix broken HTML comments that became markdown artifacts
        # Remove empty HTML comment blocks: <!-- --> or <!-- \n -->
        cleaned = re.sub(r'<!--\s*-->', '', cleaned)
        cleaned = re.sub(r'<!--\s*\n\s*-->', '', cleaned)

        # Fix malformed list formatting - standardize to proper markdown
        # Convert inconsistent list markers to standard markdown
        lines = cleaned.split('\n')
        fixed_lines = []
        for line in lines:
            # Fix lines that start with just a dash and space but aren't proper list items
            if re.match(r'^-\s*$', line.strip()):
                continue  # Skip empty list items
            # Ensure proper spacing after list markers
            line = re.sub(r'^(\s*)-([^\s])', r'\1- \2', line)
            line = re.sub(r'^(\s*)\*([^\s])', r'\1* \2', line)
            line = re.sub(r'^(\s*)\+([^\s])', r'\1+ \2', line)
            fixed_lines.append(line)
        cleaned = '\n'.join(fixed_lines)

        # Fix inconsistent heading formatting
        # Ensure proper spacing after heading markers
        cleaned = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', cleaned, flags=re.MULTILINE)

        # Fix code blocks and mathematical expressions
        # Standardize inline code formatting
        cleaned = re.sub(r'`([^`]+)`', r'`\1`', cleaned)  # Ensure proper spacing

        # Fix mathematical expressions that might have been mangled
        # Convert common mathematical notation patterns
        cleaned = re.sub(r'\\([a-zA-Z]+)', r'\\\1', cleaned)  # Preserve LaTeX commands

        # Fix code block language specifications and clean up malformed code blocks
        lines = cleaned.split('\n')
        in_code_block = False
        fixed_lines = []

        for line in lines:
            # Fix code blocks that might have malformed syntax with escaped characters
            if line.strip().startswith('```') and '\\' in line:
                # Clean up escaped characters in code block markers
                line = line.replace('\\{', '{').replace('\\}', '}')

            if line.strip().startswith('```'):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                else:
                    # Ending a code block
                    in_code_block = False
            fixed_lines.append(line)

        cleaned = '\n'.join(fixed_lines)

        # Remove manual table of contents since toc: true is set in frontmatter
        # Look for patterns that indicate a manual TOC section
        toc_patterns = [
            r'\[([^\]]+)\]\(#[^)]+\)\s*\n',  # TOC links
            r'^\[([^\]]+)\]\(#[^)]+\)$',     # Single TOC line
        ]

        # Check if we have multiple TOC-like links at the beginning
        lines = cleaned.split('\n')
        toc_end_idx = 0
        toc_link_count = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Check if this line looks like a TOC entry
            if re.match(r'^\[([^\]]+)\]\(#[^)]+\)$', stripped):
                toc_link_count += 1
                toc_end_idx = i + 1
            elif stripped == '' and toc_link_count > 0:
                # Empty line after TOC links - continue
                toc_end_idx = i + 1
            elif toc_link_count > 0 and stripped:
                # Non-empty, non-TOC line after we found TOC links
                break

        # If we found multiple TOC links (3 or more), remove them
        if toc_link_count >= 3:
            self.log(f"Removing manual TOC with {toc_link_count} links")
            lines = lines[toc_end_idx:]
            cleaned = '\n'.join(lines)

        # Remove duplicate title/author section that appears in some Google Docs exports
        # This typically appears as plain text before the first heading
        lines = cleaned.split('\n')
        content_start_idx = 0

        # Look for the first meaningful heading (# or ##)
        first_heading_idx = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r'^#{1,6}\s+', stripped):
                first_heading_idx = i
                break

        # If we found a heading, check if there's duplicate title/author before it
        if first_heading_idx > 0:
            # Look for patterns that match title/author in the first few lines
            potential_title_lines = []
            for i in range(min(5, first_heading_idx)):  # Check first 5 lines before heading
                line = lines[i].strip()
                if line and not line.startswith('#') and not line.startswith('['):
                    # Check if this looks like a title or author line
                    if (len(line) < 100 and  # Reasonable title length
                        (re.search(r'\b(properties|tensor|piezoelectric|simulation|analysis)\b', line.lower()) or  # Title keywords
                         re.search(r'\b(wentao|jiang|20\d{6})\b', line.lower()))):  # Author/date patterns
                        potential_title_lines.append(i)

            # If we found potential duplicate title/author lines, remove them
            if potential_title_lines:
                # Remove lines that look like duplicate title/author
                content_start_idx = max(potential_title_lines) + 1
                self.log(f"Removing duplicate title/author section (lines 1-{content_start_idx})")
                lines = lines[content_start_idx:]
                cleaned = '\n'.join(lines)

        # Remove empty lines that just contain whitespace or brackets
        lines = []
        for line in cleaned.split('\n'):
            stripped = line.strip()
            # Skip lines that are empty, just brackets, or just whitespace
            if stripped and stripped != '[]' and not re.match(r'^\s*\[\s*\]\s*$', stripped):
                lines.append(line.rstrip())

        cleaned = '\n'.join(lines)

        # FINAL STEP: Ensure proper spacing around images
        # Split any lines with multiple images first
        cleaned = re.sub(r'(!\[[^\]]*\]\([^)]+\))(!\[[^\]]*\]\([^)]+\))', r'\1\n\n\2', cleaned)

        # Keep splitting until no more consecutive images on same line
        while re.search(r'(!\[[^\]]*\]\([^)]+\))(!\[[^\]]*\]\([^)]+\))', cleaned):
            cleaned = re.sub(r'(!\[[^\]]*\]\([^)]+\))(!\[[^\]]*\]\([^)]+\))', r'\1\n\n\2', cleaned)

        # Now add blank lines before and after any line starting with ![
        lines = cleaned.split('\n')
        result = []

        for i, line in enumerate(lines):
            if line.strip().startswith('!['):
                # Add blank line before if previous line isn't blank
                if i > 0 and result and result[-1].strip() != '':
                    result.append('')
                result.append(line)
                # Add blank line after if next line isn't blank
                if i < len(lines) - 1 and lines[i+1].strip() != '':
                    result.append('')
            else:
                result.append(line)

        cleaned = '\n'.join(result)

        return cleaned.strip()

    def generate_front_matter(self, metadata):
        """Generate Jekyll front matter"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        front_matter = {
            'title': metadata["title"],
            'date': today,
            'categories': metadata['categories'],
            'tags': metadata['tags'],
            'toc': True,
            'use_math': True
        }

        if metadata['author']:
            front_matter['author'] = metadata["author"]
        if metadata['original_date']:
            front_matter['original_date'] = metadata['original_date']
        
        return yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)

    def save_jekyll_post(self, front_matter, markdown_content, doc_slug, created_files):
        """Save the final Jekyll post"""
        today = datetime.now().strftime('%Y-%m-%d')
        post_filename = f"{today}-{doc_slug}.md"
        post_path = self.posts_dir / post_filename

        self.log(f"Saving Jekyll post: {post_path}")

        if not self.dry_run:
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write('---\n')
                f.write(front_matter)
                f.write('---\n\n')
                f.write(markdown_content)

            created_files.append(str(post_path.relative_to(self.blog_root)))
        else:
            created_files.append(f"_posts/{post_filename}")

        return post_path

    def update_manifest(self, import_session):
        """Update the import manifest for rollback capability"""
        if self.dry_run:
            self.log("Would update manifest with import session")
            return

        manifest = {'imports': []}

        # Load existing manifest
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                manifest = yaml.safe_load(f) or {'imports': []}

        # Add new session
        manifest['imports'].append(import_session)

        # Save updated manifest
        with open(self.manifest_file, 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False)

        self.log(f"Updated manifest: {len(import_session['files_created'])} files tracked")

    def process_single_zip(self, zip_path):
        """Process a single zip file"""
        self.log(f"Processing: {zip_path}")

        try:
            # Generate document slug
            doc_slug = self.generate_slug(zip_path)
            self.log(f"Generated slug: {doc_slug}")

            # Extract zip
            extract_dir = self.extract_zip(zip_path)

            # Find HTML file
            html_file = self.find_html_file(extract_dir)

            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Copy images and get list of created files
            created_files = []
            copied_images = self.copy_images(extract_dir, doc_slug)
            created_files.extend(copied_images)

            # Clean Google Docs HTML artifacts
            cleaned_html = self.clean_google_docs_html(html_content)

            # Fix image paths in HTML
            fixed_html = self.fix_image_paths(cleaned_html, doc_slug)

            # Extract metadata
            metadata = self.extract_metadata(html_content, zip_path)
            self.log(f"Extracted metadata: {metadata['title']}")

            # Convert to markdown
            markdown_content = self.convert_to_markdown(fixed_html)

            # Generate front matter
            front_matter = self.generate_front_matter(metadata)

            # Save Jekyll post
            post_path = self.save_jekyll_post(front_matter, markdown_content, doc_slug, created_files)

            # Create import session record
            import_session = {
                'timestamp': datetime.now().isoformat(),
                'source_zip': str(zip_path),
                'doc_slug': doc_slug,
                'files_created': created_files
            }

            # Update manifest
            self.update_manifest(import_session)

            self.log(f"✅ Successfully processed: {zip_path}")
            return True

        except Exception as e:
            self.log(f"❌ Failed to process {zip_path}: {str(e)}", "ERROR")
            return False

        finally:
            # Cleanup temp directory for this zip
            if not self.dry_run and extract_dir.exists():
                shutil.rmtree(extract_dir)

    def find_zip_files(self, source_path):
        """Find all zip files in source directory"""
        source = Path(source_path)

        if source.is_file() and source.suffix == '.zip':
            return [source]
        elif source.is_dir():
            return list(source.glob('*.zip'))
        else:
            raise ValueError(f"Invalid source path: {source_path}")

    def batch_process(self, source_path):
        """Process multiple zip files"""
        zip_files = self.find_zip_files(source_path)

        if not zip_files:
            self.log("No zip files found")
            return

        self.log(f"Found {len(zip_files)} zip files to process")

        success_count = 0
        for zip_file in zip_files:
            if self.process_single_zip(zip_file):
                success_count += 1

        self.log(f"Batch complete: {success_count}/{len(zip_files)} successful")

    def rollback_last_import(self):
        """Rollback the last import session"""
        if not self.manifest_file.exists():
            self.log("No manifest file found - nothing to rollback")
            return

        with open(self.manifest_file, 'r') as f:
            manifest = yaml.safe_load(f)

        if not manifest or not manifest.get('imports'):
            self.log("No imports found in manifest")
            return

        last_import = manifest['imports'][-1]
        self.log(f"Rolling back import from {last_import['timestamp']}")

        # Delete created files
        for file_path in last_import['files_created']:
            full_path = self.blog_root / file_path
            if full_path.exists():
                if full_path.is_file():
                    full_path.unlink()
                    self.log(f"Deleted file: {file_path}")
                elif full_path.is_dir():
                    shutil.rmtree(full_path)
                    self.log(f"Deleted directory: {file_path}")

        # Remove from manifest
        manifest['imports'] = manifest['imports'][:-1]
        with open(self.manifest_file, 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False)

        self.log("✅ Rollback complete")


def main():
    parser = argparse.ArgumentParser(description='Import Google Docs HTML exports to Jekyll')
    parser.add_argument('source', nargs='?', help='Source zip file or directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--rollback', choices=['last'], help='Rollback previous import')
    parser.add_argument('--blog-root', default='.', help='Path to Jekyll blog root (default: current directory)')

    args = parser.parse_args()

    # Validate blog root
    blog_root = Path(args.blog_root).resolve()
    if not (blog_root / '_config.yml').exists():
        print(f"ERROR: {blog_root} doesn't appear to be a Jekyll blog (no _config.yml found)")
        sys.exit(1)

    importer = GoogleDocsImporter(blog_root, dry_run=args.dry_run)

    if args.rollback == 'last':
        importer.rollback_last_import()
    elif args.source:
        if Path(args.source).is_file():
            importer.process_single_zip(args.source)
        else:
            importer.batch_process(args.source)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

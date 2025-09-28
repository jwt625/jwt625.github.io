# Google Docs Batch Import for Jekyll

Converts Google Docs HTML exports (zip files) to Jekyll markdown posts with proper image handling.

## Features

- ✅ **Safe by default**: Dry-run mode prevents accidents
- ✅ **Reversible**: Full rollback capability with manifest tracking
- ✅ **Image handling**: Automatically fixes image paths for Jekyll
- ✅ **Batch processing**: Handle hundreds of documents at once
- ✅ **Smart metadata**: Auto-extracts titles, dates, and tags

## Quick Start

### 1. Install Dependencies

```bash
cd scripts/import-google-docs
pip install -r requirements.txt

# Install pandoc (required for HTML→Markdown conversion)
brew install pandoc  # macOS
# or: sudo apt install pandoc  # Ubuntu
```

### 2. Test with Single Document (Recommended)

```bash
# Dry-run first (safe - shows what would happen)
python batch_import.py --dry-run /path/to/your-document.zip

# If dry-run looks good, run for real
python batch_import.py /path/to/your-document.zip
```

### 3. Batch Process Directory

```bash
# Dry-run on entire directory
python batch_import.py --dry-run /Users/wentaojiang/Documents/Stanford/Personal/

# Process all zip files
python batch_import.py /Users/wentaojiang/Documents/Stanford/Personal/
```

## Usage Examples

### Single File Import
```bash
# Test with one of your Lithium Niobate documents
python batch_import.py --dry-run "/Users/wentaojiang/Documents/Stanford/Personal/WJ - LN properties.zip"
```

### Batch Import with Safety
```bash
# Process all zip files in directory
python batch_import.py --dry-run /path/to/zip/directory/
python batch_import.py /path/to/zip/directory/
```

### Rollback Last Import
```bash
# Undo the last import (removes all created files)
python batch_import.py --rollback last
```

## What It Does

### Input: Google Docs HTML Export
```
your-document.zip
├── YourDocument.html          # Main content
└── images/                    # Embedded images
    ├── image1.png
    ├── image2.png
    └── ...
```

### Output: Jekyll Blog Post
```
_posts/2025-09-27-your-document.md     # Markdown post
assets/images/imported/your-document/   # Images
├── image1.png
├── image2.png
└── ...
```

### Generated Front Matter
```yaml
---
title: "Your Document Title"
date: 2025-09-27
categories:
  - Research
tags:
  - Auto-detected tags
author: "Wentao Jiang"
original_date: 2018-04-28  # If found in content
toc: true
use_math: true
---
```

## Safety Features

### Dry-Run Mode
- Shows exactly what would be created
- No files are modified
- Perfect for testing before real import

### Rollback Capability
- Tracks all created files in `.import-manifest.yaml`
- One command to undo last import
- Removes both posts and images

### Error Handling
- Continues processing other files if one fails
- Clear error messages for debugging
- Preserves existing blog content

## File Organization

### Created Structure
```
your-blog/
├── _posts/
│   ├── 2025-09-27-lithium-niobate-properties.md
│   ├── 2025-09-27-piezoelectric-eigenmodes.md
│   └── ...
├── assets/images/imported/
│   ├── lithium-niobate-properties/
│   │   ├── image1.png
│   │   └── ...
│   └── piezoelectric-eigenmodes/
│       └── ...
└── .import-manifest.yaml  # Rollback tracking
```

## Troubleshooting

### Common Issues

**"Pandoc not found"**
```bash
brew install pandoc  # macOS
sudo apt install pandoc  # Ubuntu
```

**"No HTML file found"**
- Check that zip file contains `.html` file
- Some Google Docs exports may have different structure

**"Permission denied"**
- Run from blog root directory
- Check file permissions on target directories

### Debug Mode
Add `--dry-run` to any command to see what would happen without making changes.

## Advanced Usage

### Custom Blog Root
```bash
python batch_import.py --blog-root /path/to/your/blog /path/to/zips/
```

### Processing Specific Files
```bash
# Process only files matching pattern
python batch_import.py /path/to/zips/WJ*.zip
```

## What Gets Auto-Detected

### Metadata Extraction
- **Title**: From HTML `<title>` tag or first heading
- **Author**: Defaults to "Wentao Jiang"
- **Date**: Extracted from content patterns like "20180428"
- **Categories**: Defaults to "Research"
- **Tags**: Based on content keywords:
  - "Lithium Niobate" → Materials, Lithium Niobate
  - "piezoelectric" → Piezoelectric
  - "simulation" → Simulation
  - "properties" → Reference

### Image Path Fixing
Converts Google Docs relative paths to Jekyll absolute paths:
- `src="images/image1.png"` → `src="/assets/images/imported/doc-name/image1.png"`

## Next Steps

1. **Test with one document first**
2. **Review the generated markdown** 
3. **Adjust categories/tags** if needed
4. **Scale to batch processing**

The script is designed to be safe and reversible - perfect for iterative testing and refinement.

# Repository Cleanup: Removing `_site` from Git History

## Overview
This document explains the process used to remove the `_site` directory from the entire git history of the Jekyll blog repository, reducing repository size and cleaning up tracked generated files.

## Problem
- Repository size was 1.7GB due to tracking Jekyll's generated `_site` directory
- Generated HTML files were being committed to git history
- This caused unnecessary bloat and potential merge conflicts

## Solution: Git History Rewriting

### Tools Used
- **`git filter-repo`** - Modern, safe tool for rewriting git history
- **`git filter-branch`** - Alternative older method (not used)

### Step-by-Step Process

#### 1. Initial Assessment
```bash
# Check repository size
du -sh .git
# Result: 1.7G

# Identify largest files in history
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | sort -nr | head -20
# Confirmed most large files were in _site/
```

#### 2. Update .gitignore
```bash
# Uncommented lines in .gitignore:
_site/
.jekyll-metadata
```

#### 3. Remove _site from Entire Git History
```bash
# Use git filter-repo to remove _site directory from all commits
git filter-repo --path _site --invert-paths --force
```

**What this command does:**
- `--path _site` - Target the _site directory
- `--invert-paths` - Remove (rather than keep) the specified path
- `--force` - Required for safety confirmation
- Rewrites ALL commits in the repository history

#### 4. Re-add Remote and Push
```bash
# git filter-repo removes remotes for safety
git remote add origin https://github.com/jwt625/jwt625.github.io.git

# Force push the cleaned history
git push --force origin master
```

### Results

#### Before Cleanup
- `.git` directory: **1.7GB**
- Tracking generated HTML files in history
- 223 commits with _site content

#### After Cleanup
- `.git` directory: **1.6GB** (~100MB saved)
- Clean history with only source files
- All 223 commits rewritten (new SHAs)

### Important Notes

#### ⚠️ Breaking Changes
- **All commit SHAs changed** - Anyone with clones needs to re-clone
- **History rewritten** - This is a destructive operation
- **Force push required** - Overwrites remote history

#### ✅ GitHub Pages Unaffected
- GitHub builds Jekyll sites from source files
- Does NOT use local `_site` directory
- Site continues working exactly as before
- Build process unchanged

#### 🔄 Future Benefits
- Cleaner commits (only source files tracked)
- Faster git operations
- No merge conflicts from generated content
- Smaller repository size

### Alternative Approaches Considered

1. **BFG Repo-Cleaner** - Alternative tool, similar results
2. **Fresh start** - Create new repository, safer but loses history
3. **Manual cleanup** - Too time-consuming for large histories

### Verification Commands

```bash
# Check final size
du -sh .git

# Verify _site not in history
git log --name-only | grep _site
# Should return nothing

# Check current status
git status
# _site/ should be untracked (ignored)
```

### Recovery Instructions (If Needed)

If issues arise, the original repository state exists on GitHub until the force push. To recover:

1. Clone a fresh copy from GitHub (before force push)
2. Or restore from local backup if created
3. The force push overwrote the remote, so recovery requires backup

---

**Date:** 2025-07-22  
**Tool Used:** git filter-repo  
**Repository:** jwt625.github.io  
**Status:** ✅ Successfully completed

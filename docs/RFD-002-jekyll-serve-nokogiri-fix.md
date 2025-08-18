# DebugLog-000: Jekyll Serve Nokogiri Architecture Fix

**Date**: 2025-08-05  
**Issue**: Jekyll serve script failing due to Nokogiri architecture mismatch on Apple Silicon  
**Status**: ✅ RESOLVED  

## Problem Summary

The `serve.sh` script was failing to run Jekyll with the following error:
```
LoadError: cannot load such file -- nokogiri/nokogiri
```

## Root Cause Analysis

### Initial Investigation
1. **Script Location**: Found `serve.sh` (not `.serve.sh` as initially searched)
2. **Ruby Version**: System Ruby 2.6.10 (outdated)
3. **Architecture Mismatch**: Nokogiri installed for x86_64 but running on ARM64 (Apple Silicon)
4. **Bundler Version**: Old Bundler 1.17.2 incompatible with modern Ruby

### Key Error Patterns
- `nokogiri-1.13.10-x86_64-darwin` installed on `arm64` system
- `LoadError: cannot load such file -- nokogiri/nokogiri`
- Bundler compatibility issues with Ruby 3.x

## Attempted Solutions (Failed)

### 1. Bundle Reinstall with Local Path
```bash
bundle install --path vendor/bundle
```
**Result**: Still installed x86_64 version

### 2. Force Nokogiri Rebuild
```bash
bundle exec gem uninstall nokogiri
bundle config build.nokogiri --use-system-libraries
bundle install
```
**Result**: Continued to install x86_64 version

### 3. Bundle Clean and Reinstall
```bash
bundle clean --force
bundle install --path vendor/bundle
```
**Result**: Permission issues with system Ruby

## Final Solution

### 1. Install Modern Ruby Version Manager
```bash
# Install rbenv via Homebrew
brew install rbenv ruby-build

# Configure shell
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(rbenv init -)"' >> ~/.zshrc
eval "$(rbenv init -)"
```

### 2. Install Modern Ruby Version
```bash
# Install Ruby 3.3.9 (latest stable)
rbenv install 3.3.9
rbenv local 3.3.9

# Verify installation
ruby --version
# Output: ruby 3.3.9 (2025-07-24 revision f5c772fc7c) [arm64-darwin24]
```

### 3. Update RubyGems and Bundler
```bash
gem install bundler
gem update --system
```

### 4. Clean Reinstall Dependencies
```bash
# Remove old lockfile and vendor directory
rm -rf vendor/ .bundle/ Gemfile.lock

# Fresh install with new Ruby
bundle install
```

### 5. Update serve.sh Script
Enhanced the script to properly initialize rbenv:

```bash
#!/bin/bash

# Jekyll incremental build and serve script
# This script runs Jekyll with incremental builds for faster development

# Initialize rbenv if available
if command -v rbenv >/dev/null 2>&1; then
    eval "$(rbenv init -)"
fi

echo "Starting Jekyll with incremental builds..."
echo "Using Ruby: $(ruby --version)"
echo "Using Bundler: $(bundle --version)"
bundle exec jekyll serve --incremental
```

## Results

### Before Fix
- Ruby 2.6.10 (system Ruby)
- Bundler 1.17.2
- Nokogiri 1.13.10-x86_64-darwin (wrong architecture)
- Jekyll serve failing with LoadError

### After Fix
- Ruby 3.3.9 (rbenv managed)
- Bundler 2.7.1
- Nokogiri 1.18.9 (arm64-darwin) (correct architecture)
- Jekyll server running successfully at http://127.0.0.1:4000

## Key Learnings

1. **Architecture Matters**: Apple Silicon requires ARM64 native gems
2. **Ruby Version Management**: Use rbenv/asdf instead of system Ruby
3. **Clean Slate Approach**: Sometimes complete reinstall is faster than incremental fixes
4. **Script Robustness**: Include environment initialization in scripts

## Prevention

1. Use `.ruby-version` file to lock Ruby version
2. Document Ruby version requirements in README
3. Use rbenv or asdf for Ruby version management
4. Regular dependency updates to maintain compatibility

## Related Files Modified

- `serve.sh` - Enhanced with rbenv initialization
- `Gemfile.lock` - Regenerated with new Ruby/Bundler versions
- `.ruby-version` - Created (rbenv local command)

## Performance Impact

- Build time: ~27 seconds (acceptable for development)
- Incremental builds: Enabled for faster subsequent builds
- Native ARM64 performance: Significantly faster than Rosetta translation

---

## UPDATE: 2025-08-18 - Ruby Version Availability Issue

### New Problem
After the initial fix, encountered a new issue where `.ruby-version` specified `3.3.9` but this version was not available via rbenv:

```
rbenv: version `3.3.9' is not installed (set by /Users/wentaojiang/Documents/GitHub/jwt625.github.io/.ruby-version)
```

### Root Cause
- `.ruby-version` file contained `3.3.9`
- `rbenv install --list` only showed `3.3.7` as the latest available 3.3.x version
- Ruby 3.3.9 was not yet available in rbenv's ruby-build definitions

### Solution Applied
1. **Updated `.ruby-version`**: Changed from `3.3.9` to `3.3.7`
2. **Installed Ruby 3.3.7**: `rbenv install 3.3.7`
3. **Reinstalled gems**: `bundle install` to install gems for new Ruby version
4. **Verified functionality**: Jekyll serve now works correctly

### Current Working Configuration
- Ruby 3.3.7 (rbenv managed)
- Bundler 2.3.3
- All gems properly installed for ARM64 architecture
- Jekyll server running at http://127.0.0.1:4000

### Key Lesson
When specifying Ruby versions in `.ruby-version`, ensure the version is actually available via your Ruby version manager. Use `rbenv install --list | grep 3.3` to check available versions before setting the version file.

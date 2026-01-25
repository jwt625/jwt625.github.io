# RFD-008: Homepage Interactivity and Projects Timeline

## Status
**IN PROGRESS** - 2026-01-25

## DevLog

### 2026-01-25 - Timeline Visual Enhancement Implementation

**Requirements:**
1. Full-width layout on desktop (>1280px), constrained on mobile/tablet
2. Floating hover cards that don't affect layout
3. S-curve callouts connecting project boxes to axis dots
4. Time-proportional spacing based on actual time gaps
5. Alternating above/below layout for horizontal timeline
6. Mobile improvements with proper spacing and image display

**Progress:**

1. **Layout Structure**:
   - Moved timeline from `index.html` to `_layouts/default.html`
   - Positioned outside `initial-content` div, directly after masthead
   - Conditional rendering only on homepage (`page.layout == "home"`)
   - Full-width section with viewport width breakout technique
   - Breakpoint at 1280px for mobile/tablet constraint

2. **CSS Implementation** (`assets/css/projects-timeline.css`):
   - Full-width container styling with dark background (#1a1a1a)
   - Horizontal layout: axis-centered dots, alternating boxes above/below
   - Vertical layout: left-aligned axis, boxes on right
   - SVG connector positioning for S-curves (horizontal) and straight lines (vertical)
   - Floating detail cards with absolute positioning
   - Responsive breakpoints at 1280px and 768px

3. **JavaScript Implementation** (`assets/js/projects-timeline.js`):
   - Time-proportional spacing: 50px (0-2mo), 100px (3-6mo), 150px (7-12mo), 200px (>1yr)
   - S-curve SVG path generation for horizontal connectors
   - Dynamic spacing applied via inline styles
   - Separate rendering paths for horizontal vs vertical layouts

**Current Status:**
- Placement and size correct
- Timeline positioned flush below masthead
- Full-width on desktop, constrained on mobile

**Known Issues:**
- Rendering and aesthetic problems remain
- Interactivity issues need fixing
- Further refinement required

### 2026-01-25 - Bug Fixes and Completion

**Bugs Fixed:**
1. Missing data file: Created `data/paginated-posts-non-ofs.json` that was referenced but didn't exist
   - Filters out OFS posts using `{% raw %}{% unless post.categories contains 'OFS' %}{% endraw %}` logic
   - Generates 55 non-OFS posts across 11 pages (vs 137 total posts across 28 pages)
2. Missing thumbnails: Added `cover` field to both JSON data files
   - Updated `data/paginated-posts-all.json` and `data/paginated-posts-non-ofs.json` to include `post.header.cover`
   - Modified `createPostElement()` in `assets/js/ofs-toggle.js` to render cover images
3. Unnecessary category tags: Removed category display from JavaScript-rendered posts
   - Deleted category badge rendering from `createPostElement()` function

**Status:**
- OFS toggle fully functional with proper pagination
- Thumbnails display correctly in both all-posts and non-OFS views
- Clean post listings without category badges on homepage

### 2026-01-25 - Initial Implementation and Redesign

**Completed:**
- Phase 1: OFS Toggle Feature (Initial - BROKEN)
  - Created `assets/js/ofs-toggle.js` with toggle logic and localStorage persistence
  - Created `assets/css/ofs-toggle.css` with floating button styling
  - Modified `_layouts/default.html` to include OFS toggle scripts
  - Button appears on homepage, toggles OFS post visibility, state persists via localStorage

- Phase 2: Projects Timeline Feature
  - Created `_data/projects.yml` with 30+ projects (milestones, playground, spun-off projects)
  - Created `assets/js/projects-timeline.js` with timeline rendering and zoom/pan controls
  - Created `assets/css/projects-timeline.css` with responsive dark theme styling
  - Created `_includes/projects-timeline.html` as timeline container
  - Created `data/projects.json` as JSON endpoint for JavaScript
  - Modified `index.html` to include timeline component
  - Timeline displays at top of homepage with controls and hover interactions

**Critical Issues Identified:**

1. **OFS Toggle - Pagination Problem:**
   - Initial implementation used client-side filtering with `display: none`
   - Jekyll pagination is static (5 posts per page, built at compile time)
   - When hiding OFS posts, pages show inconsistent numbers of visible posts
   - Example: Page 1 shows only 1 non-OFS post (if 4 out of 5 posts are OFS)
   - This breaks the expected pagination behavior

2. **OFS Toggle - Scope Problem:**
   - Toggle button only appears on homepage (path `/`, `/index.html`, `/page\d+/`)
   - Paginated pages (`/page2/`, `/page3/`, etc.) do not show the toggle button
   - This is due to `isHomepage()` check in `assets/js/ofs-toggle.js` line 20-24

**Root Cause:**
Client-side filtering is fundamentally incompatible with static Jekyll pagination. The pagination is pre-rendered with 5 posts per page. Hiding posts client-side leaves gaps but does not fetch additional posts to fill the page.

**Failed Approach:**
Attempted to create Jekyll plugin (`_plugins/paginated_posts_generator.rb`) to generate JSON files with pagination data for client-side rendering. This was overengineered and missed the point - Jekyll already generates static pages, so we should leverage that instead of fighting it with client-side hacks.

**Correct Solution (To Be Implemented):**

Replace `jekyll-paginate` with `jekyll-paginate-v2` and generate two separate sets of static paginated pages at build time:
1. `/` - all posts (current behavior)
2. `/non-ofs/` - only non-OFS posts (filtered by category)

The toggle button will navigate between these two URL spaces (e.g., from `/page3/` to `/non-ofs/page3/`) instead of hiding posts client-side.

Benefits:
- Both views have proper pagination (5 posts per page)
- Everything is static HTML generated at build time
- No complex JavaScript or plugins needed
- Toggle button works on all paginated pages
- Consistent layout in both states

This is the "run it twice with different filters" approach - Jekyll generates both sets of pages during build.

## Problem Statement

The blog homepage currently lacks two key features:
1. No ability to filter/hide OFS (Outside Five Sigma) weekly posts, which can bury actual technical writings
2. No visual representation of side projects deployed across multiple subdomains

## Requirements

### Feature 1: OFS Posts Toggle

**User Story**: As a reader, I want to hide/show OFS weekly posts to focus on technical articles.

**Specifications**:
- Location: Right sidebar (floating, follows scroll like existing RAG chat widget)
- Default state: OFS posts hidden
- Persistence: Toggle state saved in localStorage
- Scope: Homepage only (not archive pages)
- Implementation: Client-side JavaScript filtering

**Reference**: Existing chat widget implementation at `assets/js/blog-chat-widget.js` and `assets/css/blog-chat-widget.css`

### Feature 2: Projects Timeline

**User Story**: As a visitor, I want to see a visual timeline of projects to understand the breadth of work.

**Specifications**:
- Location: Top of homepage, above post listings
- Data source: `_data/projects.yml` (manually curated)
- Timeline range: Default last 6 months, scrollable to first project
- Interactivity: Zoom, pan, click to navigate
- Hover behavior: Show detail card with description, links, preview image
- Mobile: Switch to vertical layout
- Preview images: Leave blank if unavailable

**Project Sources**:
- All folders from PlayGround repo (100+ projects)
- Spun-off projects: TabTreeTracker, BPM, VoiceModeTranscript, bay-bridge-traffic-cam, 3dgs-viewer, GDSJam, psh, claude-code-inspector, SLM-Guessr
- Additional undocumented repos: age-of-agents, WC3-sounds, ra2-sounds, magic-crystals, QFC-plot
- Historical context from About page (chemistry at 13, physics/math in high school, nanofab 2015-2024, current IoT/CV/robotics)

**Date Extraction**:
- PlayGround folders: Parse date from folder name (e.g., `20230903_travelTime` -> 2023-09-03)
- Spun-off projects: Use GitHub creation date or milestone date
- Historical milestones: Extract from About page narrative

## Design Decisions

### OFS Toggle Design
- Follows existing chat widget pattern for consistency
- Hidden by default to prioritize technical content
- localStorage prevents toggle reset on navigation
- Homepage-only scope keeps implementation simple

### Timeline Design
- Horizontal timeline for desktop (better for date visualization)
- Vertical for mobile (better for scrolling)
- Manual YAML data file (more control than GitHub API, no rate limits)
- Blank images acceptable (avoids placeholder clutter)
- No filtering/classification initially (keep simple, add later if needed)

## Implementation Plan

### Phase 1: OFS Toggle (Simpler, implement first)

**Files to create/modify**:
1. `assets/js/ofs-toggle.js` - Toggle logic and localStorage handling
2. `assets/css/ofs-toggle.css` - Floating button styling (match chat widget)
3. `_layouts/default.html` - Add toggle button and script includes
4. `_includes/ofs-toggle.html` - Toggle button HTML structure

**Implementation approach**:
- Add `data-category` attribute to post elements during Jekyll build
- JavaScript filters posts by checking category attribute
- CSS transitions for smooth show/hide
- localStorage key: `ofs_posts_visible`

### Phase 2: Projects Timeline

**Files to create/modify**:
1. `_data/projects.yml` - Project metadata (name, date, description, links, image)
2. `assets/js/projects-timeline.js` - Timeline rendering and interaction
3. `assets/css/projects-timeline.css` - Timeline styling (dark theme compatible)
4. `_includes/projects-timeline.html` - Timeline container and template
5. `index.html` - Include timeline component

**Timeline library options**:
- vis-timeline (feature-rich, good zoom/pan)
- timelinejs (simpler, good for storytelling)
- Custom D3.js implementation (full control, more work)

**Data structure** (`_data/projects.yml`):
```yaml
- name: "TabTreeTracker"
  date: "2024-10"
  description: "Chrome extension for tab navigation history visualization"
  links:
    - url: "https://github.com/jwt625/TabTreeTracker"
      label: "GitHub"
  image: "/assets/images/projects/TTT.png"
  category: "spun-off"
```

**Mobile responsiveness**:
- CSS media query at 768px breakpoint
- Switch from horizontal to vertical layout
- Adjust touch interactions for mobile

## Technical References

### Existing Codebase
- Jekyll config: `_config.yml` (Minimal Mistakes theme v4.26.2, dark skin)
- Post structure: `_posts/*.md` with front matter categories
- Chat widget: `assets/js/blog-chat-widget.js` (floating sidebar pattern)
- Custom styles: `_sass/custom/custom.scss`
- Layout: `_layouts/default.html` (injection point for new features)
- Homepage: `index.html` (uses `layout: home`)

### External Resources
- PlayGround repo: https://github.com/jwt625/PlayGround
- About page: `_pages/about.md` (historical timeline context)
- Minimal Mistakes docs: https://mmistakes.github.io/minimal-mistakes/
- Timeline libraries: vis-timeline, timelinejs, D3.js

### Post Categories
- OFS posts: `categories: - OFS`
- Other categories: Blog, Tutorial, Research, Teardown
- Category archive: `_pages/category-archive.md`

## Success Criteria

- OFS toggle button visible and functional on homepage
- Toggle state persists across page reloads
- Timeline displays all projects with correct dates
- Timeline zoom/pan works smoothly
- Hover cards show project details
- Mobile layout switches to vertical
- Dark theme styling consistent with blog
- No performance degradation on homepage load

## Related Documents

- RFD-000-ephemeral-rag-chat-widget.md (chat widget implementation pattern)
- README.md (blog technical overview)
- _pages/about.md (historical context for timeline)


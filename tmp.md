# Frontend RAG Chat Widget Implementation Notes

## Overview
Successfully implemented an ephemeral RAG chat widget for Jekyll blog with dark theme styling and CORS integration.

## Frontend Implementation

### Files Created
1. **`assets/js/blog-chat-widget.js`** - Main widget JavaScript (emoji-free, production-ready)
2. **`assets/css/blog-chat-widget.css`** - Dark theme styling with sharp corners
3. **`_plugins/environment_variables.rb`** - Jekyll plugin for environment variables
4. **`_layouts/default.html`** - Modified to include widget scripts and config

### Key Features Implemented
- **Floating chat button** - Fixed position, dark theme colors
- **Modal dialog** - Sharp corners, dark background (#2c3e50)
- **Rate limiting** - 30 seconds between requests
- **Error handling** - Detailed error messages with expandable details
- **Loading states** - Spinner animation during API calls
- **Responsive design** - Works on desktop and mobile
- **Keyboard navigation** - Enter to submit, click outside to close
- **Source references** - Shows relevance scores and clickable links
- **Markdown rendering** - Basic markdown support for responses

### Dark Theme Color Scheme
- **Background**: #2c3e50 (main), #34495e (header/buttons)
- **Text**: #ecf0f1 (primary), #bdc3c7 (secondary)
- **Borders**: #4a5f7a
- **Links**: #5dade2
- **Error**: #e74c3c

### Environment Variable Configuration
- **Local Development**: Uses `.env` file with `CHATBOT_API_URL`
- **Production**: GitHub Repository Variables (planned)
- **Setup Script**: `scripts/setup-local-dev.sh` loads environment

## CORS Debug Process

### Initial Problem
```
Access to fetch at 'http://146.235.193.141:8000/rag/generate-test' from origin 'http://localhost:4000' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### Debug Steps
1. **Confirmed API works via curl** - Ruled out API server issues
2. **Identified CORS preflight issue** - Browser sends OPTIONS request before POST
3. **Tested CORS headers** - Found missing `Access-Control-Allow-Origin` header

### CORS Testing Commands
```bash
# Test OPTIONS preflight request
curl -X OPTIONS http://146.235.193.141:8000/rag/generate-test \
  -H "Origin: http://localhost:4000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

# Test actual POST request
curl -X POST http://146.235.193.141:8000/rag/generate-test \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:4000" \
  -d '{"query": "test", "context_limit": 3}' \
  -v
```

### CORS Headers Analysis
**Required headers found:**
- ✅ `access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT`
- ✅ `access-control-allow-headers: Content-Type`
- ✅ `access-control-allow-credentials: true`

**Missing critical header:**
- ❌ `Access-Control-Allow-Origin: http://localhost:4000`

## API Server CORS Configuration

### FastAPI (Python) - Working Solution:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4000",
        "http://127.0.0.1:4000",
        "https://jwt625.github.io"  # For production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
```

### Why CORS is Complex
1. **Browser Security**: Same-Origin Policy prevents cross-domain requests
2. **Preflight Requests**: Browser sends OPTIONS request for "complex" requests
3. **Content-Type Trigger**: `application/json` triggers preflight
4. **Origin Matching**: Server must explicitly allow the requesting origin

### Key Learnings
- **curl vs Browser**: curl has no CORS restrictions, browsers do
- **Preflight Required**: POST with JSON content-type always triggers preflight
- **Exact Origin Match**: CORS origin must match exactly (localhost vs 127.0.0.1)
- **Missing Headers**: All required CORS headers must be present

## Final Status
✅ **Widget Working**: Chat widget successfully integrated and functional
✅ **CORS Resolved**: API server properly configured with CORS headers
✅ **Dark Theme**: Consistent styling with blog's dark theme
✅ **Error Handling**: Comprehensive error messages and debugging
✅ **Rate Limiting**: 30-second cooldown between requests

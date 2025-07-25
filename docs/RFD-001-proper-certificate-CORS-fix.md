# Setting up HTTPS for FastAPI on OCI Instance

## Problem
Your RAG chat widget is experiencing a Mixed Content Error because:
- GitHub Pages serves your site over HTTPS
- Your FastAPI API only supports HTTP
- Browsers block HTTP requests from HTTPS sites for security

## Solution: Enable HTTPS on your OCI Instance

### Architecture
```
Internet → your-domain.com:443 (HTTPS) → Nginx → localhost:8000 (FastAPI HTTP)
```

## Step-by-Step Setup

### 1. Install Nginx on your OCI Instance
```bash
# SSH into your OCI instance
ssh your-username@146.235.193.141

# Install Nginx
sudo apt update
sudo apt install nginx  # Ubuntu/Debian
# OR
sudo yum install nginx  # CentOS/RHEL
```

### 2. Configure Nginx
Create a new configuration file:
```bash
sudo nano /etc/nginx/sites-available/rag-api.outside5sigma.com
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name rag-api.outside5sigma.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name rag-api.outside5sigma.com;

    # SSL certificates (will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/rag-api.outside5sigma.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/rag-api.outside5sigma.com/privkey.pem;

    # Proxy all requests to your FastAPI app
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Let FastAPI handle CORS - don't add nginx CORS headers
        # This prevents duplicate CORS headers that cause browser errors
    }
}
```

### 3. Enable the Site
```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/rag-api.outside5sigma.com /etc/nginx/sites-enabled/

# Test the configuration
sudo nginx -t

# Start/restart Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 4. Update OCI Security Rules
In OCI Console → Compute → Instances → Your Instance → Subnet → Security Lists:

Add ingress rules:
- **Port 80** (HTTP) - Source: 0.0.0.0/0
- **Port 443** (HTTPS) - Source: 0.0.0.0/0

### 5. Get Free SSL Certificate with Let's Encrypt
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate for your subdomain
sudo certbot --nginx -d rag-api.outside5sigma.com
```

**This single command will:**
- ✅ Get a free SSL certificate from Let's Encrypt
- ✅ Automatically configure Nginx to use it
- ✅ Set up automatic renewal (every 90 days)
- ✅ Redirect HTTP to HTTPS

### 6. Keep FastAPI Running
Your FastAPI continues running on port 8000 (HTTP internally):
```bash
# Your FastAPI command stays the same
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. Update Jekyll Configuration
After HTTPS is working, update `_layouts/default.html`:
```javascript
// Chat widget configuration
// Using subdomain for RAG API - no more exposed IP addresses!
window.CHAT_CONFIG = {
  apiUrl: 'https://rag-api.outside5sigma.com'
};
```

## Prerequisites
- Subdomain `rag-api.outside5sigma.com` pointing to your OCI instance IP
- Ports 80 and 443 open in OCI security rules
- FastAPI running on port 8000

## Why This Works
- **Nginx** acts as a reverse proxy handling HTTPS termination
- **Let's Encrypt** provides free, trusted SSL certificates
- **Automatic renewal** keeps certificates current
- **CORS headers** allow your GitHub Pages site to access the API

## Testing
1. Visit `https://rag-api.outside5sigma.com/rag/generate-test` - should work over HTTPS
2. Test the chat widget on your GitHub Pages site - no more Mixed Content Error
3. Check certificate: `openssl s_client -connect rag-api.outside5sigma.com:443`

## Troubleshooting
- **Domain not pointing to server**: Update DNS A record for `rag-api.outside5sigma.com` in Cloudflare
- **Ports blocked**: Check OCI security lists and instance firewall
- **Nginx errors**: Check logs with `sudo journalctl -u nginx`
- **Certificate issues**: Run `sudo certbot renew --dry-run`

## Next Steps
Once HTTPS is working:
1. Update the API URL in your Jekyll site
2. Test the chat widget functionality
3. Set up automatic certificate renewal monitoring

## CORS Configuration for FastAPI

### Problem
If you get CORS errors like:
```
Access to fetch at 'https://rag-api.outside5sigma.com/rag/generate-test' from origin 'http://localhost:4000' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: The 'Access-Control-Allow-Origin' header contains multiple values 'http://localhost:4000, https://jwt625.github.io', but only one is allowed.
```

This means your FastAPI server is sending multiple CORS headers, which browsers reject.

### Solution: Configure CORS in FastAPI

Add this to your FastAPI application (usually in `main.py`):

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:4000",           # Local Jekyll development
    "http://127.0.0.1:4000",          # Alternative localhost
    "https://outside5sigma.com",       # Your main site
    "https://jwt625.github.io",        # GitHub Pages (if still used)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Your existing routes...
```

### Alternative: Allow All Origins (Less Secure)
For development/testing only:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - use only for testing
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
```

### Remove Nginx CORS Headers
Make sure your nginx configuration does NOT include CORS headers:

```nginx
# In your nginx config, remove these lines if present:
# add_header Access-Control-Allow-Origin "..." always;
# add_header Access-Control-Allow-Methods "..." always;
# add_header Access-Control-Allow-Headers "..." always;
```

Let FastAPI handle all CORS configuration to avoid conflicts.

### Restart Services
After making changes:

```bash
# Restart your FastAPI application
# (however you're running it - systemd, screen, etc.)

# Test nginx config and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Testing CORS
Test from browser console on both:
- `http://localhost:4000` (local development)
- `https://outside5sigma.com` (production)

Both should work without CORS errors.

## Mobile Browser CORS Preflight Fix

### Problem Identified
Mobile Safari and Firefox on iPhone are failing with:
```
Preflight response is not successful. Status code: 400
Fetch API cannot load https://rag-api.outside5sigma.com/rag/generate-test due to access control checks.
```

This indicates the API server is returning status 400 for CORS preflight (OPTIONS) requests, which mobile browsers send before POST requests.

### Required Server-Side Fix

Your FastAPI server needs to properly handle CORS preflight requests:

#### 1. Handle OPTIONS Requests Explicitly
Add this to your FastAPI application:

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4000",
        "http://127.0.0.1:4000",
        "https://outside5sigma.com",
        "https://jwt625.github.io",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
    max_age=86400,  # Cache preflight for 24 hours
)

# Explicit OPTIONS handler for the RAG endpoint
@app.options("/rag/generate-test")
async def preflight_handler(request: Request):
    """Handle CORS preflight requests for mobile browsers"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept",
            "Access-Control-Max-Age": "86400",
        }
    )
```

#### 2. Ensure POST Endpoint Returns Correct CORS Headers
Make sure your existing POST endpoint includes proper headers:

```python
@app.post("/rag/generate-test")
async def generate_test(request: YourRequestModel):
    # Your existing logic here
    response_data = {"answer": "...", "context_used": [...]}

    # Return with explicit CORS headers for mobile compatibility
    return JSONResponse(
        content=response_data,
        headers={
            "Access-Control-Allow-Origin": "*",  # Or specific origin
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept",
        }
    )
```

#### 3. Debug Preflight Requests
Add logging to see what's happening:

```python
import logging

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    logging.info(f"Headers: {dict(request.headers)}")

    response = await call_next(request)

    logging.info(f"Response status: {response.status_code}")
    return response
```

### Key Requirements for Mobile CORS:
1. **OPTIONS requests must return status 200** (not 400)
2. **Preflight response must include all required CORS headers**
3. **Access-Control-Max-Age should be set** to reduce preflight requests
4. **No duplicate CORS headers** (FastAPI only, not Nginx)

### Testing After Fix:
1. Deploy the updated FastAPI code
2. Test on iPhone Safari again
3. Should see successful OPTIONS request followed by successful POST request

The issue is definitely server-side - mobile browsers are correctly following CORS specifications that the server isn't properly supporting.

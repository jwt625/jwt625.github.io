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

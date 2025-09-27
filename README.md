# 🛡️ ModSecurity WAF + Docker Security Stack

A comprehensive Web Application Firewall (WAF) implementation using ModSecurity, Nginx, and Docker containerization to protect web applications against common security threats.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Testing](#testing)
- [Security Features](#security-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This project demonstrates a production-ready security stack that combines:
- **Docker containerization** for application isolation
- **ModSecurity WAF** for web application protection
- **Nginx reverse proxy** with SSL/TLS termination
- **OWASP Core Rule Set** for comprehensive threat detection

The setup protects a Flask web application against OWASP Top 10 vulnerabilities including SQL injection, Cross-Site Scripting (XSS), and command injection attacks.

## Architecture

```
[Client] → [Nginx + ModSecurity WAF] → [Docker Container (Flask App)]
    ↓              ↓                         ↓
  HTTPS         SSL Termination         Isolated Environment
 Request       Threat Detection         Application Runtime
```

### Components:
- **Frontend**: Nginx with ModSecurity module
- **Security Layer**: OWASP Core Rule Set (CRS)
- **Application**: Dockerized Flask application
- **Encryption**: Self-signed SSL certificates

## Features

-  **Web Application Firewall** - ModSecurity with OWASP CRS
-  **Docker Containerization** - Isolated application environment
-  **SSL/TLS Encryption** - HTTPS with self-signed certificates
-  **Threat Protection** - Real-time attack detection and blocking
-  **Logging & Monitoring** - Comprehensive security event logging
-  **Reverse Proxy** - Nginx load balancing and request routing
-  **Attack Prevention** - SQL injection, XSS, command injection protection

## Prerequisites

- Ubuntu Server 20.04+ or similar Linux distribution
- Root or sudo access
- Minimum 2GB RAM
- 10GB free disk space
- Basic knowledge of Docker and Nginx

## Installation

### Step 1: Server Setup

Update the system and install Docker:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
sudo apt install -y docker.io docker-compose

# Enable Docker service
sudo systemctl enable docker --now

# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Create application directory
mkdir app
```

### Step 2: Application Deployment

Transfer your Flask application to the server:

```bash
# From client PC - copy Flask app to server
scp ~/Documents/BUG_BOUNTY/Millisec_Test/app.py user@x.x.x.x:~/app
```

### Step 3: Docker Container Setup

Create and configure the Dockerfile:

```bash
cd app
```

Create `Dockerfile`:
```dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Baku

RUN apt update && \ 
    apt full-upgrade -y && \
    apt install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install flask                    
COPY . /app/

EXPOSE 5000
CMD ["python3", "app.py"]
```

Build and run the Docker container:

```bash
# Build Docker image
docker build -t app .

# Run container (bind to localhost only for security)
docker run -d --name app -p 127.0.0.1:5000:5000 app
```

### Step 4: ModSecurity Installation

Install build dependencies:

```bash
sudo apt update && sudo apt upgrade
sudo apt install gcc make build-essential autoconf automake libtool \
libcurl4-openssl-dev liblua5.3-dev libfuzzy-dev ssdeep gettext \
pkg-config libgeoip-dev libyajl-dev doxygen libpcre++-dev \
libpcre2-16-0 libpcre2-dev libpcre2-posix3 zlib1g zlib1g-dev -y
```

Compile ModSecurity from source:

```bash
# Clone ModSecurity repository
cd /opt && sudo git clone https://github.com/owasp-modsecurity/ModSecurity.git
cd ModSecurity

# Initialize and update submodules
sudo git submodule init
sudo git submodule update

# Build and install ModSecurity
sudo ./build.sh
sudo ./configure
sudo make
sudo make install
```

### Step 5: Nginx + ModSecurity Module

Clone the Nginx connector:

```bash
cd /opt && sudo git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git
```

Install Nginx:

```bash
# Add Nginx PPA for latest version
sudo add-apt-repository ppa:ondrej/nginx -y
sudo apt update
sudo apt install nginx -y
sudo systemctl enable nginx

# Verify Nginx version
sudo nginx -v
# Expected: nginx version: nginx/1.28.0
```

Compile Nginx with ModSecurity module:

```bash
# Download Nginx source
cd /opt && sudo wget https://nginx.org/download/nginx-1.28.0.tar.gz
sudo tar -xzvf nginx-1.28.0.tar.gz
cd nginx-1.28.0

# Configure with ModSecurity module
sudo ./configure --with-compat --add-dynamic-module=/opt/ModSecurity-nginx
sudo make
sudo make modules

# Install the module
sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules-enabled/
```

## Configuration

### ModSecurity Configuration

Copy configuration files:

```bash
sudo cp /opt/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsecurity.conf
sudo cp /opt/ModSecurity/unicode.mapping /etc/nginx/unicode.mapping
```

Load ModSecurity module in Nginx:

```bash
# Add to /etc/nginx/nginx.conf (at the top)
echo "load_module /etc/nginx/modules-enabled/ngx_http_modsecurity_module.so;" | sudo tee -a /etc/nginx/nginx.conf
```

### SSL Certificate Generation

Create self-signed SSL certificate:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/app.key \
    -out /etc/ssl/certs/app.crt \
    -subj "/CN=app.com"
```

### Nginx Virtual Host Configuration

Configure `/etc/nginx/sites-enabled/default`:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name app.org;
    return 301 https://$server_name$request_uri;
}

# HTTPS server with ModSecurity
server {
    listen 443 ssl;
    server_name app.org;
    
    ssl_certificate /etc/ssl/certs/app.crt;
    ssl_certificate_key /etc/ssl/private/app.key;
    
    # Enable ModSecurity WAF
    modsecurity on;
    modsecurity_rules_file /etc/nginx/modsecurity.conf;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### OWASP Core Rule Set (CRS)

Enable ModSecurity engine:

```bash
echo "SecRuleEngine On" | sudo tee -a /etc/nginx/modsecurity.conf
```

Install OWASP CRS:

```bash
# Clone OWASP Core Rule Set
sudo git clone https://github.com/coreruleset/coreruleset.git /etc/nginx/owasp-crs

# Copy setup configuration
sudo cp /etc/nginx/owasp-crs/crs-setup.conf{.example,}

# Include CRS rules in ModSecurity config
cat >> /etc/nginx/modsecurity.conf << EOF
Include owasp-crs/crs-setup.conf
Include owasp-crs/rules/*.conf
EOF
```

Restart Nginx:

```bash
# Test configuration
sudo nginx -t

# Restart Nginx service
sudo systemctl restart nginx
```

## Testing

### Client Setup

Configure client machine:

```bash
# Add hostname resolution (on client PC)
echo "192.168.50.190 app.org" | sudo tee -a /etc/hosts
```

### Security Tests

Test normal functionality:

```bash
# Test HTTPS connection
curl -k https://app.org/
```

Test WAF protection:

```bash
# Test command injection (should be blocked)
curl -k https://app.org/?q=/bin/bash

# Test SQL injection (should be blocked)
curl -k "https://app.org/?id=1' OR '1'='1"

# Test XSS attack (should be blocked)
curl -k "https://app.org/?input=<script>alert('xss')</script>"
```

### Expected Results

- Normal requests: **200 OK** response
- Malicious requests: **403 Forbidden** or **406 Not Acceptable**
- All attempts logged in `/var/log/nginx/error.log`

## Security Features

### Threat Protection
- **SQL Injection Prevention**
- **Cross-Site Scripting (XSS) Blocking**
- **Command Injection Detection**
- **Directory Traversal Protection**
- **HTTP Protocol Violations**
- **Malicious User Agent Detection**

### Monitoring & Logging
- Real-time attack detection
- Detailed security event logging
- IP-based blocking capabilities
- Request/response inspection

### Performance Features
- Reverse proxy caching
- Load balancing ready
- SSL termination
- Compression support

## Troubleshooting

### Common Issues

1. **ModSecurity module not loading:**
   ```bash
   # Check if module exists
   ls -la /etc/nginx/modules-enabled/ngx_http_modsecurity_module.so
   
   # Verify Nginx configuration
   sudo nginx -t
   ```

2. **SSL certificate errors:**
   ```bash
   # Regenerate certificates
   sudo rm /etc/ssl/private/app.key /etc/ssl/certs/app.crt
   # Re-run certificate generation command
   ```

3. **Docker container not accessible:**
   ```bash
   # Check container status
   docker ps -a
   
   # View container logs
   docker logs app
   ```

4. **WAF blocking legitimate requests:**
   ```bash
   # Check ModSecurity logs
   tail -f /var/log/nginx/error.log
   
   # Adjust rules in /etc/nginx/modsecurity.conf
   ```

### Log Locations

- **Nginx Access Logs**: `/var/log/nginx/access.log`
- **Nginx Error Logs**: `/var/log/nginx/error.log`
- **ModSecurity Audit Logs**: `/var/log/modsec_audit.log`
- **Docker Logs**: `docker logs app`

## Advanced Configuration

### Custom ModSecurity Rules

Add custom rules to `/etc/nginx/modsecurity.conf`:

```apache
# Custom rule example - block specific user agents
SecRule REQUEST_HEADERS:User-Agent "@contains badbot" \
    "id:1001,phase:1,deny,msg:'Bad bot detected'"
```

### Performance Tuning

Optimize for high traffic:

```nginx
# Add to nginx.conf
worker_processes auto;
worker_connections 1024;

# Enable compression
gzip on;
gzip_vary on;
gzip_types text/plain text/css application/json application/javascript text/xml;
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [ModSecurity Documentation](https://github.com/SpiderLabs/ModSecurity)
- [OWASP Core Rule Set](https://github.com/coreruleset/coreruleset)
- [Nginx ModSecurity Module](https://github.com/SpiderLabs/ModSecurity-nginx)
- [Docker Documentation](https://docs.docker.com/)

---

**Security Notice**: This setup uses self-signed certificates suitable for development/testing. For production environments, use certificates from a trusted Certificate Authority (CA).

**Support**: For issues and questions, please open an issue in this repository.

# Deployment Guide - LULC Recognition Dashboard

Complete guide for deploying the LULC Recognition system to production environments.

## Deployment Options

### Option 1: Docker (Recommended for Production)

#### Prerequisites
- Docker installed
- Docker Compose installed
- Git for version control

#### Single Command Deployment

```bash
# Build and run both services
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

#### Production Configuration

1. **Update environment variables**:
   ```bash
   cp .env.example .env.production
   # Edit .env.production with production URLs
   ```

2. **Build images**:
   ```bash
   docker-compose -f docker-compose.yml build
   ```

3. **Run with production settings**:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

4. **Check health**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:3000
   ```

---

### Option 2: Vercel (Frontend Only) + Cloud VM (Backend)

#### Deploy Frontend to Vercel

1. **Connect repository to Vercel**:
   - Go to https://vercel.com/new
   - Connect GitHub repository
   - Configure environment: `NEXT_PUBLIC_API_URL=https://your-backend-url`

2. **Deploy**:
   ```bash
   vercel deploy --prod
   ```

3. **Automatic deployments**:
   - Vercel auto-deploys on push to main branch
   - Preview deployments for pull requests

#### Deploy Backend to Cloud VM (AWS EC2 example)

1. **Create EC2 instance**:
   ```bash
   # Ubuntu 22.04 LTS, t3.medium or larger
   # Open ports 8000 (backend), 80 (HTTP), 443 (HTTPS)
   ```

2. **SSH into instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**:
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python 3.11
   sudo apt install -y python3.11 python3.11-venv python3-pip
   
   # Install other tools
   sudo apt install -y git curl nginx
   ```

4. **Clone and setup backend**:
   ```bash
   cd /home/ubuntu
   git clone https://github.com/your-repo/lulc-dashboard.git
   cd lulc-dashboard/backend
   
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -e .
   
   # Create models directory and copy your .pth files
   mkdir -p models
   # Copy your trained models here
   cp /path/to/eurosat_fold4.pth models/
   cp /path/to/mlrsnet_fold3.pth models/
   cp /path/to/patternnet_fold3.pth models/
   ```

5. **Setup systemd service**:
   ```bash
   # Create service file
   sudo nano /etc/systemd/system/lulc-backend.service
   ```
   
   ```ini
   [Unit]
   Description=LULC Recognition Backend
   After=network.target
   
   [Service]
   Type=notify
   User=ubuntu
   WorkingDirectory=/home/ubuntu/lulc-dashboard/backend
   Environment="PATH=/home/ubuntu/lulc-dashboard/backend/venv/bin"
   ExecStart=/home/ubuntu/lulc-dashboard/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   # Enable and start service
   sudo systemctl daemon-reload
   sudo systemctl enable lulc-backend
   sudo systemctl start lulc-backend
   
   # Check status
   sudo systemctl status lulc-backend
   ```

6. **Setup Nginx reverse proxy**:
   ```bash
   sudo nano /etc/nginx/sites-available/lulc-backend
   ```
   
   ```nginx
   upstream lulc_backend {
       server 127.0.0.1:8000;
   }
   
   server {
       listen 80;
       server_name your-domain.com;
   
       # Redirect to HTTPS
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl http2;
       server_name your-domain.com;
   
       # SSL certificates (use Let's Encrypt)
       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
   
       location / {
           proxy_pass http://lulc_backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           
           # Increase timeout for large uploads
           proxy_read_timeout 300s;
           proxy_connect_timeout 75s;
       }
   }
   ```
   
   ```bash
   # Enable site
   sudo ln -s /etc/nginx/sites-available/lulc-backend /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **Setup SSL (Let's Encrypt)**:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot certonly --nginx -d your-domain.com
   ```

---

### Option 3: Heroku (Deprecated but still available)

Note: Heroku free tier was discontinued. For low-cost options, use Railway or Render instead.

#### Using Railway

1. **Create account on Railway**:
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy backend**:
   ```bash
   # Install Railway CLI
   curl -i https://railway.app/install.sh | bash
   
   # Login
   railway login
   
   # Deploy
   cd backend
   railway up
   ```

3. **Configure environment**:
   ```bash
   railway variables set PYTHONUNBUFFERED=1
   ```

4. **Get public URL**:
   ```bash
   railway domain
   ```

5. **Update frontend**:
   - Set `NEXT_PUBLIC_API_URL` in Vercel environment variables

---

### Option 4: AWS ECS (Containerized)

1. **Build Docker images**:
   ```bash
   # Build backend
   docker build -t lulc-backend:latest backend/
   
   # Build frontend
   docker build -f Dockerfile.frontend -t lulc-frontend:latest .
   ```

2. **Push to ECR**:
   ```bash
   # Create ECR repositories
   aws ecr create-repository --repository-name lulc-backend
   aws ecr create-repository --repository-name lulc-frontend
   
   # Login
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   
   # Tag and push backend
   docker tag lulc-backend:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/lulc-backend:latest
   docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/lulc-backend:latest
   
   # Tag and push frontend
   docker tag lulc-frontend:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/lulc-frontend:latest
   docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/lulc-frontend:latest
   ```

3. **Create ECS cluster and tasks**:
   - Create ECS cluster in AWS console
   - Create task definitions for backend and frontend
   - Create services with load balancers

---

## Pre-Deployment Checklist

- [ ] All tests pass locally
- [ ] Environment variables configured
- [ ] Models files ready (.pth files)
- [ ] Database backups (if applicable)
- [ ] SSL certificates obtained
- [ ] Domain DNS configured
- [ ] Rate limiting configured
- [ ] Monitoring setup
- [ ] Error tracking (Sentry)
- [ ] Logging configured

---

## Environment Variables

### Backend (.env or system environment)
```bash
# Server
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# Optional: Force CPU (comment out for GPU)
# CUDA_VISIBLE_DEVICES=""

# Optional: Custom host/port
# HOST=0.0.0.0
# PORT=8000
```

### Frontend (.env.local or Vercel environment)
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

---

## Monitoring & Logging

### Backend Logging
```bash
# View logs
sudo journalctl -u lulc-backend -f

# Or with Docker
docker logs -f lulc-backend
```

### Health Checks
```bash
# API health
curl https://api.yourdomain.com/health

# Swagger UI
https://api.yourdomain.com/docs
```

### Performance Monitoring
```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 https://api.yourdomain.com/health

# Or with wrk
wrk -t4 -c100 -d30s https://api.yourdomain.com/health
```

---

## Scaling Strategies

### Database-less Application (Current)
- **Horizontal**: Add load balancer, multiple backend instances
- **Vertical**: Upgrade instance size (CPU, RAM, GPU)
- **Caching**: Redis for model cache (if shared instances)

### With Large Traffic
1. **Frontend**: CDN (CloudFront, Cloudflare)
2. **Backend**: Load balancer (AWS ALB, nginx)
3. **Models**: GPU instances for faster inference
4. **Database**: Add if user data needed

---

## Security Best Practices

### HTTPS
```bash
# Force HTTPS in nginx
server {
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### Rate Limiting
```nginx
# In nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

### CORS in Production
```python
# In backend app.py
CORSMiddleware(
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Secret Management
```bash
# Use environment variables for secrets
# Never commit API keys or credentials
echo "SECRET_KEY=your_secret" >> .env
# Add .env to .gitignore
```

---

## Database Backups (If Added)

```bash
# PostgreSQL example
sudo pg_dump -U postgres lulc_db > backup.sql

# Restore
psql -U postgres lulc_db < backup.sql

# Schedule backups with cron
0 2 * * * /usr/local/bin/backup-db.sh
```

---

## Zero-Downtime Deployment

### Blue-Green Deployment
1. Deploy new version to "green" environment
2. Test thoroughly
3. Switch traffic from "blue" to "green"
4. Keep "blue" as rollback

### Rolling Updates with Docker Swarm
```bash
docker service update --image lulc-backend:new lulc-backend-service
```

---

## Rollback Procedure

### Docker
```bash
# List image versions
docker images lulc-backend

# Run previous version
docker run -d -p 8000:8000 lulc-backend:previous
```

### Systemd
```bash
# Restart with previous code
cd /home/ubuntu/lulc-dashboard
git checkout previous-tag
systemctl restart lulc-backend
```

---

## Performance Tuning

### Backend Optimization
```python
# Increase workers for more concurrency
uvicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend Optimization
```bash
# Build with optimizations
pnpm build
# Analyze bundle
pnpm build --analyze
```

### Infrastructure Tuning
```bash
# Increase file descriptors (Linux)
ulimit -n 65535

# Tune kernel parameters
sysctl -w net.core.somaxconn=65535
```

---

## Monitoring Solutions

### Error Tracking (Sentry)
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
)
```

### Application Performance Monitoring (DataDog)
```bash
# Backend with DataDog
DD_SERVICE=lulc-backend \
DD_ENV=production \
DD_TRACE_ENABLED=true \
uvicorn app:app
```

### Uptime Monitoring
```bash
# Use services like:
# - UptimeRobot (free tier)
# - Pingdom
# - StatusCake
```

---

## Cost Optimization

### AWS
- Use auto-scaling for variable load
- Use spot instances for non-critical workloads
- Reserved instances for baseline load
- CloudFront CDN for static assets

### Vercel
- Free tier: 100GB bandwidth/month
- Pro tier: $20/month for unlimited

### Cloud VM
- Use smallest instance for low traffic
- Use auto-scaling groups
- Use reserved instances for committed usage

---

## Support & Debugging

### Common Issues

**Backend not starting**
```bash
# Check logs
journalctl -u lulc-backend -n 100

# Check if port is in use
lsof -i :8000

# Verify models exist
ls -la backend/models/
```

**CORS errors**
```bash
# Check frontend URL in backend CORS config
# Ensure NEXT_PUBLIC_API_URL matches backend domain
```

**Slow inference**
```bash
# Check if GPU is being used
nvidia-smi

# Check CPU usage
top

# Analyze inference time via API
curl http://localhost:8000/docs  # Try /predict
```

---

## Disaster Recovery

### Backup Strategy
1. **Code**: Git repository (GitHub)
2. **Models**: Backup storage (S3/GCS)
3. **Data**: Database backups (daily)
4. **Configuration**: Version control

### Recovery Plan
1. Clone repository from GitHub
2. Restore models from backup storage
3. Restore database from backup
4. Redeploy infrastructure

---

## Conclusion

The LULC Recognition Dashboard is designed for easy deployment across multiple platforms. Start with Docker for simplicity, then scale to cloud platforms as needed.

For production deployments, always:
- ✅ Use HTTPS
- ✅ Configure monitoring
- ✅ Setup logging
- ✅ Plan for backups
- ✅ Use auto-scaling
- ✅ Test thoroughly before deployment

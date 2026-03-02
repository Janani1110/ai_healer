# Deployment Guide

## Production Deployment

### Prerequisites

- Server with Docker and Docker Compose
- Domain name (optional but recommended)
- SSL certificate (for HTTPS)
- CI/CD platform credentials
- OpenAI API key with sufficient credits

### Deployment Options

## Option 1: Docker Compose (Recommended)

### 1. Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y
```

### 2. Clone Repository

```bash
git clone <repository-url>
cd self-healing-ci-agent
```

### 3. Configure Environment

```bash
cp .env.example .env
nano .env
```

**Production .env:**
```env
# CI/CD Platforms
GITHUB_TOKEN=ghp_production_token
GITLAB_TOKEN=glpat_production_token

# AI Configuration
OPENAI_API_KEY=sk-production_key
AI_MODEL=gpt-4

# Agent Configuration
AGENT_PORT=8000
POLLING_INTERVAL=30
AUTO_FIX_ENABLED=true
AUTO_COMMIT_ENABLED=true
MAX_RETRY_ATTEMPTS=3

# Database (use PostgreSQL in production)
DATABASE_URL=postgresql://user:password@db:5432/ci_healer

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/agent.log

# Dashboard
DASHBOARD_PORT=3000
```

### 4. Update Docker Compose for Production

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ci_healer
      POSTGRES_USER: agent
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  agent:
    build: ./agent-core
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://agent:${DB_PASSWORD}@db:5432/ci_healer
      GITHUB_TOKEN: ${GITHUB_TOKEN}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: always

  dashboard:
    build: ./dashboard
    depends_on:
      - agent
    ports:
      - "80:3000"
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - dashboard
    restart: always

volumes:
  postgres_data:
```

### 5. Deploy

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 6. Verify Deployment

```bash
# Check services
docker-compose ps

# Check logs
docker-compose logs -f agent

# Test API
curl http://localhost:8000/health
```

## Option 2: Kubernetes

### 1. Create Kubernetes Manifests

**k8s/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ci-healer-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ci-healer-agent
  template:
    metadata:
      labels:
        app: ci-healer-agent
    spec:
      containers:
      - name: agent
        image: ci-healer-agent:latest
        env:
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: ci-healer-secrets
              key: github-token
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ci-healer-secrets
              key: openai-key
        ports:
        - containerPort: 8000
```

### 2. Create Secrets

```bash
kubectl create secret generic ci-healer-secrets \
  --from-literal=github-token=ghp_xxx \
  --from-literal=openai-key=sk-xxx
```

### 3. Deploy

```bash
kubectl apply -f k8s/
```

## Option 3: Cloud Platforms

### AWS ECS

1. Build and push Docker images to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure load balancer
5. Set up CloudWatch logging

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/ci-healer-agent

# Deploy
gcloud run deploy ci-healer-agent \
  --image gcr.io/PROJECT_ID/ci-healer-agent \
  --platform managed \
  --region us-central1 \
  --set-env-vars GITHUB_TOKEN=xxx,OPENAI_API_KEY=xxx
```

### Azure Container Instances

```bash
az container create \
  --resource-group ci-healer \
  --name ci-healer-agent \
  --image ci-healer-agent:latest \
  --environment-variables \
    GITHUB_TOKEN=xxx \
    OPENAI_API_KEY=xxx
```

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Nginx Configuration

**nginx.conf:**
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://dashboard:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://agent:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Database Migration

### From SQLite to PostgreSQL

```bash
# Export data
sqlite3 agent.db .dump > backup.sql

# Import to PostgreSQL
psql -U agent -d ci_healer < backup.sql
```

## Monitoring Setup

### Prometheus Metrics

Add to agent:
```python
from prometheus_client import Counter, Histogram, start_http_server

failures_detected = Counter('failures_detected', 'Total failures detected')
fixes_applied = Counter('fixes_applied', 'Total fixes applied')
fix_duration = Histogram('fix_duration_seconds', 'Time to apply fix')
```

### Grafana Dashboard

Import dashboard JSON for visualization.

## Backup Strategy

### Database Backups

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump -U agent ci_healer > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://backups/ci-healer/
```

### Configuration Backups

```bash
# Backup configs
tar -czf config_backup.tar.gz config/ .env
```

## Scaling Considerations

### Horizontal Scaling

- Run multiple agent instances
- Use message queue for coordination
- Implement distributed locking

### Vertical Scaling

- Increase container resources
- Optimize database queries
- Cache frequently accessed data

## Security Hardening

1. **Network Security**
   - Use VPC/private networks
   - Configure firewall rules
   - Enable DDoS protection

2. **Access Control**
   - Implement authentication
   - Use role-based access
   - Enable audit logging

3. **Secrets Management**
   - Use AWS Secrets Manager / Azure Key Vault
   - Rotate credentials regularly
   - Never commit secrets to git

4. **Container Security**
   - Use minimal base images
   - Scan for vulnerabilities
   - Run as non-root user

## Health Checks

### Kubernetes Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Docker Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

## Troubleshooting

### Common Issues

**Agent not detecting failures:**
- Check API credentials
- Verify network connectivity
- Review polling interval

**Fixes not being applied:**
- Check git credentials
- Verify repository permissions
- Review auto-fix settings

**High memory usage:**
- Reduce polling frequency
- Limit concurrent fixes
- Optimize database queries

### Log Analysis

```bash
# View agent logs
docker-compose logs -f agent

# Search for errors
docker-compose logs agent | grep ERROR

# Monitor in real-time
tail -f logs/agent.log
```

## Maintenance

### Regular Tasks

- Monitor disk space
- Review and rotate logs
- Update dependencies
- Check API rate limits
- Review fix success rates

### Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose build

# Restart services
docker-compose up -d
```

## Cost Optimization

1. **OpenAI API**
   - Use GPT-3.5 for simple analyses
   - Cache common error patterns
   - Implement rate limiting

2. **Infrastructure**
   - Use spot instances
   - Scale down during off-hours
   - Optimize container sizes

3. **Database**
   - Archive old records
   - Implement data retention policy
   - Use read replicas for queries

# Docker Deployment Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- GoTo Connect Developer Account with OAuth app configured

### 1. Environment Setup

Create a `.env` file in the project root:

```bash
# GoTo Connect OAuth Configuration (REQUIRED)
GOTO_CLIENT_ID=your_client_id_here
GOTO_CLIENT_SECRET=your_client_secret_here
GOTO_REDIRECT_URI=http://your-server-ip:5000/callback

# Application Configuration (OPTIONAL)
SECRET_KEY=your-secret-key-change-this
APP_TITLE=GoTo Device Location Manager
LOG_LEVEL=INFO
SESSION_TIMEOUT=3600
```

### 2. Deploy with Docker Compose

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The application will be available at `http://localhost:5000`

## Manual Docker Build

### Build the Image

```bash
# Build the Docker image
docker build -t goto-device-manager .

# Run the container
docker run -d \
  --name goto-device-manager \
  -p 5000:5000 \
  -e GOTO_CLIENT_ID=your_client_id \
  -e GOTO_CLIENT_SECRET=your_client_secret \
  -e GOTO_REDIRECT_URI=http://your-server:5000/callback \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  --restart unless-stopped \
  goto-device-manager
```

## Unraid Installation

### Option 1: Community Apps (Recommended)

1. Install the "Community Applications" plugin in Unraid
2. Search for "GoTo Device Manager"
3. Click "Install" and configure the required settings:
   - **GoTo Client ID**: Your OAuth Client ID
   - **GoTo Client Secret**: Your OAuth Client Secret  
   - **Redirect URI**: Update with your Unraid server IP
   - **Port**: 5000 (or change if needed)
   - **Data/Log Paths**: Default paths are recommended

### Option 2: Manual Template Installation

1. Download the template file: `unraid-template.xml`
2. In Unraid web interface, go to **Docker** → **Add Container**
3. In the "Template" dropdown, select "Upload Template"
4. Upload the `unraid-template.xml` file
5. Configure the required environment variables
6. Click "Apply" to create the container

### Unraid Configuration

**Required Settings:**
- **Container Name**: goto-device-manager
- **Port**: 5000 → 5000 (or your preferred port)
- **GOTO_CLIENT_ID**: Your GoTo Connect OAuth Client ID
- **GOTO_CLIENT_SECRET**: Your GoTo Connect OAuth Client Secret
- **GOTO_REDIRECT_URI**: `http://YOUR_UNRAID_IP:5000/callback`

**Storage Paths:**
- **Data**: `/mnt/user/appdata/goto-device-manager/data`
- **Logs**: `/mnt/user/appdata/goto-device-manager/logs`
- **Config**: `/mnt/user/appdata/goto-device-manager/config` (optional)

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOTO_CLIENT_ID` | Yes | - | GoTo Connect OAuth Client ID |
| `GOTO_CLIENT_SECRET` | Yes | - | GoTo Connect OAuth Client Secret |
| `GOTO_REDIRECT_URI` | Yes | `http://localhost:5000/callback` | OAuth redirect URI |
| `SECRET_KEY` | No | Auto-generated | Flask session secret key |
| `APP_TITLE` | No | `GoTo Device Location Manager` | Application title |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `SESSION_TIMEOUT` | No | `3600` | Session timeout in seconds |

## Volume Mounts

| Container Path | Purpose | Recommended Host Path |
|----------------|---------|----------------------|
| `/app/data` | Application data storage | `./data` or `/mnt/user/appdata/goto-device-manager/data` |
| `/app/logs` | Application logs | `./logs` or `/mnt/user/appdata/goto-device-manager/logs` |
| `/app/config` | Configuration files (optional) | `./config` or `/mnt/user/appdata/goto-device-manager/config` |

## Health Checks

The container includes built-in health checks that verify the application is responding correctly. You can check the health status with:

```bash
docker inspect --format='{{.State.Health.Status}}' goto-device-manager
```

## Troubleshooting

### Container Won't Start

1. Check Docker logs:
   ```bash
   docker logs goto-device-manager
   ```

2. Verify environment variables are set correctly
3. Ensure port 5000 isn't already in use
4. Check file permissions on volume mounts

### OAuth Issues

1. Verify `GOTO_CLIENT_ID` and `GOTO_CLIENT_SECRET` are correct
2. Ensure `GOTO_REDIRECT_URI` matches your actual server address
3. Check that the redirect URI is registered in your GoTo Connect OAuth app

### Performance Tuning

For high-traffic deployments, you can modify the Gunicorn configuration by overriding the CMD:

```bash
docker run -d \
  # ... other options ...
  goto-device-manager \
  gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

## Security Considerations

1. **Use HTTPS in production**: Configure a reverse proxy (nginx, Traefik) with SSL
2. **Secure environment variables**: Use Docker secrets or encrypted environment files
3. **Network isolation**: Place container in a dedicated Docker network
4. **Regular updates**: Keep the container image updated
5. **Access control**: Implement proper firewall rules

## Backup and Recovery

### Backing Up Data

```bash
# Backup application data
tar -czf goto-backup-$(date +%Y%m%d).tar.gz ./data ./logs

# For Unraid users
tar -czf goto-backup-$(date +%Y%m%d).tar.gz /mnt/user/appdata/goto-device-manager/
```

### Restoring Data

```bash
# Stop the container
docker-compose down

# Restore data
tar -xzf goto-backup-YYYYMMDD.tar.gz

# Start the container
docker-compose up -d
```

## Support

For issues, feature requests, or contributions:
- GitHub Issues: [Project Repository]
- Documentation: [Project Wiki]
- Community: [Discord/Forum Link]
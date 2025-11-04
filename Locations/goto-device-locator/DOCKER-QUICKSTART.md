# 🐳 Quick Docker Setup

## TL;DR - Get Started in 3 Steps

### 1. Set up your environment
```bash
cp .env.docker .env
# Edit .env with your GoTo Connect credentials
```

### 2. Build and run
```bash
./docker-build.sh build
./docker-build.sh run
```

### 3. Access your app
Open http://localhost:5000 in your browser!

---

## 🎯 Unraid Users

1. **Community Apps Plugin**: Search for "GoTo Device Manager"
2. **Configure**: Set your GoTo Connect OAuth credentials
3. **Install**: Click apply and you're done!

**Required settings for Unraid:**
- **GOTO_CLIENT_ID**: Your OAuth Client ID
- **GOTO_CLIENT_SECRET**: Your OAuth Client Secret  
- **GOTO_REDIRECT_URI**: `http://YOUR_UNRAID_IP:5000/callback`

---

## 📋 What You Get

- **Production-ready**: Multi-stage Docker build with Gunicorn
- **Security**: Non-root user, health checks, secure defaults
- **Persistence**: Data and logs persist across container restarts
- **Easy deployment**: One-command setup with docker-compose
- **Unraid integration**: Ready-to-use community app template

## 📚 Full Documentation

See [DOCKER.md](DOCKER.md) for complete deployment guide, troubleshooting, and advanced configuration options.

---

**Need GoTo Connect OAuth credentials?**
Visit the [GoTo Developer Portal](https://developer.goto.com/) to create an OAuth application.
# 🏢 GoTo Connect Device Location Manager

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

A comprehensive web application for managing GoTo Connect devices, locations, and phone numbers. Built with Flask and featuring a responsive design, Docker deployment, and Unraid integration.

## ✨ Features

### 🔐 **Secure Authentication**
- OAuth 2.0 integration with GoTo Connect
- Automatic token refresh
- Session management

### 📍 **Location Management**
- View all locations in your organization
- Emergency service information
- Address and contact details
- Device assignments per location

### 📱 **Device Management**
- Real-time device status monitoring
- Device details and specifications
- Remote device operations (reboot, resync)
- Bulk device management tools
- Network and license information

### 📞 **Phone Number Administration**
- Complete phone number inventory
- Extension management
- Assignment tracking
- Routing configuration
- Feature and capability overview

### 🎨 **Modern Interface**
- Responsive design for all devices
- Mobile-optimized layouts
- Bootstrap 5 UI framework
- Intuitive navigation

### 🐳 **Easy Deployment**
- Docker containerization
- Unraid community app template
- One-command setup
- Production-ready configuration

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/goto-device-locator.git
cd goto-device-locator

# Set up environment
cp .env.docker .env
# Edit .env with your GoTo Connect credentials

# Build and run
./docker-build.sh build
./docker-build.sh run

# Access at http://localhost:5000
```

### Option 2: Unraid

1. Install **Community Applications** plugin
2. Search for **"GoTo Device Manager"**
3. Configure your OAuth credentials
4. Click **Apply** - Done! 🎉

### Option 3: Manual Installation

```bash
# Clone repository
git clone https://github.com/your-username/goto-device-locator.git
cd goto-device-locator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run application
python app.py
```

## 📋 Prerequisites

### GoTo Connect Setup
1. **GoTo Connect Account** with API access
2. **Developer Portal Access** at [developer.goto.com](https://developer.goto.com/)
3. **OAuth Application** configured with appropriate scopes

### Required OAuth Scopes
- `voice:administration:devices:read`
- `voice:administration:devices:write`
- `voice:administration:locations:read`
- `voice:administration:phone-numbers:read`
- `voice:administration:extensions:read`

### System Requirements
- **Python 3.11+** (for manual installation)
- **Docker & Docker Compose** (for containerized deployment)
- **Modern web browser** with JavaScript enabled

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GOTO_CLIENT_ID` | ✅ | OAuth Client ID | `abc123...` |
| `GOTO_CLIENT_SECRET` | ✅ | OAuth Client Secret | `def456...` |
| `GOTO_REDIRECT_URI` | ✅ | OAuth Redirect URI | `http://localhost:5000/callback` |
| `SECRET_KEY` | ⚠️ | Flask session key | Auto-generated if not set |
| `APP_TITLE` | ❌ | Custom app title | `My Device Manager` |
| `LOG_LEVEL` | ❌ | Logging level | `INFO` |

### OAuth Application Setup

1. Visit [GoTo Developer Portal](https://developer.goto.com/)
2. Create new OAuth application
3. Set redirect URI: `http://your-domain:5000/callback`
4. Note your Client ID and Client Secret
5. Configure required scopes (see above)

## 🐳 Docker Deployment

### Quick Start
```bash
# Build and run with one command
./docker-build.sh run
```

### Manual Docker Commands
```bash
# Build image
docker build -t goto-device-manager .

# Run container
docker run -d \
  --name goto-device-manager \
  -p 5000:5000 \
  -e GOTO_CLIENT_ID=your_client_id \
  -e GOTO_CLIENT_SECRET=your_client_secret \
  -e GOTO_REDIRECT_URI=http://localhost:5000/callback \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  goto-device-manager
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

For detailed Docker documentation, see [DOCKER.md](DOCKER.md).

## 🏠 Unraid Installation

### Community App Template
The easiest way to deploy on Unraid is through the Community Applications plugin:

1. **Install Plugin**: Add Community Applications plugin
2. **Search**: Look for "GoTo Device Manager"
3. **Configure**: Set your OAuth credentials
4. **Deploy**: Click Apply

### Manual Template Installation
1. Download `unraid-template.xml`
2. Import in Unraid Docker settings
3. Configure environment variables
4. Set volume mappings

See [DOCKER.md](DOCKER.md) for complete Unraid setup guide.

## 📱 Usage

### First Time Setup
1. Access the application at `http://localhost:5000`
2. Click **"Login with GoTo Connect"**
3. Authorize the application
4. Enter your Account Key in the dashboard
5. Start exploring your devices and locations!

### Main Features

#### 📍 **Location Management**
- View all organizational locations
- See emergency service configurations
- Browse devices assigned to each location
- Access detailed location information

#### 📱 **Device Operations**
- Monitor real-time device status
- View detailed device specifications
- Perform remote operations (reboot, resync)
- Bulk device management
- License and network information

#### 📞 **Phone Number Administration**
- Complete phone number inventory
- Extension assignments and routing
- Feature and capability overview
- Integration with device assignments

#### 🔧 **Advanced Features**
- Device-location mapping visualization
- Bulk operations on multiple devices
- Detailed logging and monitoring

## 🛡️ Security

### Authentication
- OAuth 2.0 with PKCE (Proof Key for Code Exchange)
- Automatic token refresh
- Secure session management
- No passwords stored locally

### Data Protection
- All API communications over HTTPS
- Session tokens encrypted
- Local data stored securely
- No sensitive data in logs

### Docker Security
- Non-root user execution
- Minimal attack surface
- Health checks enabled
- Resource limitations

## 🔧 Development

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/your-username/goto-device-locator.git
cd goto-device-locator

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your credentials

# Run in development mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Project Structure
```
goto-device-locator/
├── app/
│   ├── services/          # API service classes
│   ├── templates/         # Jinja2 templates
│   └── static/            # CSS, JS, images
├── docker-build.sh        # Docker helper script
├── docker-compose.yml     # Docker Compose config
├── Dockerfile            # Docker build instructions
├── requirements.txt      # Python dependencies
└── unraid-template.xml   # Unraid community app template
```

### API Service Architecture
- **GoToAPIService**: Core API integration
- **AuthService**: OAuth authentication handling
- **Config**: Application configuration management

## 🐛 Troubleshooting

### Common Issues

#### Authentication Fails
- Verify Client ID and Secret are correct
- Check redirect URI matches exactly
- Ensure OAuth app has required scopes

#### Device Operations Don't Work
- Confirm account key is set correctly
- Check API permissions in GoTo Connect
- Verify device IDs are valid

#### Container Won't Start
- Check environment variables are set
- Verify port 5000 isn't in use
- Review Docker logs: `docker logs goto-device-manager`

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/your-username/goto-device-locator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/goto-device-locator/discussions)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use descriptive commit messages
- Include docstrings for functions
- Update documentation when needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GoTo Connect** for providing the comprehensive API
- **Bootstrap** for the responsive UI framework
- **Flask** for the excellent web framework
- **Docker** for containerization capabilities

## 🔗 Links

- **GoTo Connect**: [goto.com](https://goto.com)
- **Developer Portal**: [developer.goto.com](https://developer.goto.com)
- **API Documentation**: [developer.goto.com/api](https://developer.goto.com/api)

---

**⭐ Star this repository if you find it useful!**
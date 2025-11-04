#!/bin/bash
set -e

# GoTo Connect Device Location Manager Docker Entrypoint

echo "Starting GoTo Connect Device Location Manager..."

# Create necessary directories
mkdir -p /app/logs /app/data /app/config

# Set default environment variables if not provided
export FLASK_ENV=${FLASK_ENV:-production}
export FLASK_DEBUG=${FLASK_DEBUG:-0}
export SECRET_KEY=${SECRET_KEY:-$(python -c "import secrets; print(secrets.token_hex(32))")}
export APP_TITLE="${APP_TITLE:-GoTo Device Location Manager}"
export LOG_LEVEL=${LOG_LEVEL:-INFO}

# Validate required environment variables
if [ -z "$GOTO_CLIENT_ID" ]; then
    echo "WARNING: GOTO_CLIENT_ID environment variable is not set"
    echo "Please set this to your GoTo Connect OAuth Client ID"
fi

if [ -z "$GOTO_CLIENT_SECRET" ]; then
    echo "WARNING: GOTO_CLIENT_SECRET environment variable is not set"
    echo "Please set this to your GoTo Connect OAuth Client Secret"
fi

# Set redirect URI if not provided
if [ -z "$GOTO_REDIRECT_URI" ]; then
    echo "WARNING: GOTO_REDIRECT_URI not set, using default"
    export GOTO_REDIRECT_URI="http://localhost:5000/callback"
fi

# Create .env file from environment variables for the application
cat > /app/.env << EOF
# GoTo Connect OAuth Configuration
GOTO_CLIENT_ID=${GOTO_CLIENT_ID}
GOTO_CLIENT_SECRET=${GOTO_CLIENT_SECRET}
GOTO_REDIRECT_URI=${GOTO_REDIRECT_URI}

# Application Configuration
SECRET_KEY=${SECRET_KEY}
FLASK_ENV=${FLASK_ENV}
FLASK_DEBUG=${FLASK_DEBUG}
APP_TITLE=${APP_TITLE}
LOG_LEVEL=${LOG_LEVEL}
SESSION_TIMEOUT=${SESSION_TIMEOUT:-3600}
EOF

echo "Configuration loaded:"
echo "  - App Title: ${APP_TITLE}"
echo "  - Environment: ${FLASK_ENV}"
echo "  - Debug Mode: ${FLASK_DEBUG}"
echo "  - Log Level: ${LOG_LEVEL}"
echo "  - Redirect URI: ${GOTO_REDIRECT_URI}"

# Wait for any dependencies (if needed)
echo "Checking application health..."

# Run database migrations or setup if needed
# (Add any initialization scripts here)

echo "Starting application with command: $@"

# Execute the main command
exec "$@"
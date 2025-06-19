#!/bin/bash

PROJECT_NAME="clipperAI"
PROJECT_DIR="/home/ubuntu/$PROJECT_NAME"
VENV_DIR="$PROJECT_DIR/venv"
DJANGO_SETTINGS_MODULE="$PROJECT_NAME.settings"
GUNICORN_SOCKET="/run/$PROJECT_NAME.sock"
GUNICORN_USER="ubuntu"
GUNICORN_GROUP="www-data"

echo "🔧 Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv nginx

echo "🐍 Creating virtual environment..."
cd "$PROJECT_DIR"
python3 -m venv venv
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install django gunicorn

echo "🧪 Collecting static files..."
python manage.py collectstatic --noinput

echo "🛠️ Creating Gunicorn systemd service..."
sudo tee /etc/systemd/system/$PROJECT_NAME.service > /dev/null <<EOF
[Unit]
Description=gunicorn daemon for $PROJECT_NAME
After=network.target

[Service]
User=$GUNICORN_USER
Group=$GUNICORN_GROUP
WorkingDirectory=$PROJECT_DIR
ExecStart=$VENV_DIR/bin/gunicorn --access-logfile - --workers 3 --bind unix:$GUNICORN_SOCKET $PROJECT_NAME.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

echo "🚦 Enabling and starting Gunicorn..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable $PROJECT_NAME
sudo systemctl start $PROJECT_NAME
sudo systemctl status $PROJECT_NAME

echo "🌐 Setting up Nginx config..."
sudo tee /etc/nginx/sites-available/$PROJECT_NAME > /dev/null <<EOF
server {
    listen 80;
    server_name 18.233.97.177;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $PROJECT_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$GUNICORN_SOCKET;
    }
}
EOF

echo "🔗 Enabling Nginx site and restarting..."
sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx

echo "✅ Setup complete! Your Django app should be live."

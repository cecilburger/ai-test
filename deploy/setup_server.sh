#!/bin/bash
# Run this on the server after uploading files

set -e

APP_DIR=/var/www/garuda-chatbot

echo "=== Installing system packages ==="
apt-get update -y
apt-get install -y python3 python3-pip python3-venv nginx

echo "=== Setting up app directory ==="
mkdir -p $APP_DIR

echo "=== Creating virtual environment ==="
python3 -m venv $APP_DIR/venv

echo "=== Installing Python dependencies ==="
$APP_DIR/venv/bin/pip install --upgrade pip
$APP_DIR/venv/bin/pip install flask python-dotenv gunicorn torch transformers

echo "=== Training intent model ==="
cd $APP_DIR && $APP_DIR/venv/bin/python train_model.py

echo "=== Configuring nginx ==="
cp $APP_DIR/deploy/nginx.conf /etc/nginx/sites-available/garuda-chatbot
ln -sf /etc/nginx/sites-available/garuda-chatbot /etc/nginx/sites-enabled/garuda-chatbot
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "=== Setting up systemd service ==="
cp $APP_DIR/deploy/garuda-chatbot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable garuda-chatbot
systemctl restart garuda-chatbot

echo "=== Done! ==="
systemctl status garuda-chatbot
echo ""
echo "App is running at http://72.62.244.186"

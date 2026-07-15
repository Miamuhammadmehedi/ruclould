#!/bin/bash
clear
echo "========================================="
echo "      Installing RuvCloud Tool...        "
echo "========================================="
termux-setup-storage
pkg update && pkg upgrade -y
pkg install python openssh -y
pip install colorama
chmod +x ruvcloud.py
echo ""
echo "[✓] Setup complete! Put your HTML files in /RuvCloud/www/ and run 'python ruvcloud.py'"
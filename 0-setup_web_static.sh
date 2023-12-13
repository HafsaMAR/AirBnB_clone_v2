#!/usr/bin/env bash
# Script to automate setting the web servers for the deployment of web_static

#exit code in case of error
trap 'exit 0' ERR

#check whether the nginx is installed
if ! command -v nginx &> /dev/null; then
    sudo apt update
    sudo -y apt install nginx
fi

#create folders if not existant
sudo mkdir -p "/data/web_static/releases/test/"
sudo mkdir -p "/data/web_static/shared/"

body="My acker website under construction! Welcome back later!"
date=$(date + "%Y-%m-%d %H:%M:%S")
html_content="<html>
<head></head>
<body>$body</body>
<p> it is $date</p>
</html>"

echo "$html_content" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# remove the current symbolic link and create a new one
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# change permission of the /data/
sudo chown -R ubuntu:ubuntu /data/

sudo wget -q -O /data/web_static/current/ http://exampleconfig.com/static/raw/nginx/ubuntu20.04/etc/nginx/sites-available/default

config="/etc/nginx/sites-available/default"

sudo sed -i '/^}$/i '
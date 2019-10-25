#!/bin/sh

apt update
apt install software-properties-common -y
add-apt-repository universe
add-apt-repository ppa:certbot/certbot
apt update

apt install nginx certbot python-certbot-nginx docker.io docker-compose -y


cd /root || exit
git clone https://github.com/HackTheMidlands/announcements.git
cd announcements || exit
mv /root/token.pickle token.pickle
docker-compose up -d --build

rm /etc/nginx/sites-enabled/default
mv deploy/live.nginx.txt /etc/nginx/sites-available/live
ln -s /etc/nginx/sites-available/live /etc/nginx/sites-enabled/
echo "client_max_body_size 25M;" > /etc/nginx/conf.d/client-size.conf
sudo systemctl restart nginx

certbot --non-interactive --nginx --redirect --domains live.hackthemidlands.com --agree-tos --register-unsafely-without-email
sudo systemctl restart nginx
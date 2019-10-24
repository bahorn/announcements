#!/bin/sh
apt update -qq
apt install -y -qq docker.io docker-compose
cd /root || exit
git clone https://github.com/HackTheMidlands/announcements.git app
mv token.pickle app/
cd app || exit
git checkout test-terraform
docker-compose up -d
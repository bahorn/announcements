#!/bin/sh

git clone https://github.com/HackTheMidlands/announcements.git
cp token.pickle announcements/
cd announcements || exit
git checkout test-terraform
docker-compose up -d
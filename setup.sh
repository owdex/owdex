#!/bin/bash

echo "Setting up your Owdex development installation."
echo "This should not be used in production. See https://github.com/owdex/compose."

# cd to script location, just in case
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Checking for prerequisites..."
docker --version > /dev/null || (echo "Docker not installed!"; exit 1)
docker compose --help > /dev/null || (echo "Docker compose not installed!"; exit 1)
pre-commit --version > /dev/null || (echo "Pre-commit not installed!"; exit 1)
npm --version > /dev/null || (echo "NPM not installed!"; exit 1)

echo "Setting up pre-commit hooks..."
npm install > /dev/null
pre-commit install > /dev/null

echo "Creating data folders if they don't exist..."
mkdir -p ./data/solr
mkdir -p ./data/mongo

echo "Purging existing misc files..."
rm -rf ./misc

echo "Creating misc directory..."
mkdir -p ./misc

echo "Downloading configuration files..."
wget -q "https://github.com/owdex/compose/archive/refs/heads/main.zip" -O /tmp/compose-main.zip
unzip -qq /tmp/compose-main.zip -d /tmp
mv /tmp/compose-main/owdex.toml .
mv /tmp/compose-main/misc/solr_configset /tmp/compose-main/misc/solr_entrypoint.sh ./misc
rm -rf /tmp/compose-main.zip /tmp/compose-main

echo "Setting permissions..."
sudo chown -R 8983 ./data/solr

echo "All done. Happy searching!"

exit

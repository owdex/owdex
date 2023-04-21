#!/bin/bash

echo "Setting up your Owdex development installation."
echo "This should not be used in production. See https://github.com/owdex/compose."

# cd to script location, just in case
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Checking for prerequisites..."
pre-commit --version > /dev/null || exit 1
npm --version > /dev/null || exit 1

echo "Setting up pre-commit hooks..."
npm install --silent
pre-commit install > /dev/null

echo "Creating data folders if they don't exist..."
mkdir -p ./data/solr
mkdir -p ./data/mongo

echo "Purging existing misc files..."
rm -rf ./misc

echo "Creating misc directory..."
mkdir -p ./misc

echo "Downloading configuration files..."
wget -q "https://github.com/owdex/compose/archive/refs/heads/link-overhaul.zip" -O /tmp/compose-link-overhaul.zip
unzip -q /tmp/compose-link-overhaul.zip -d /tmp
mv /tmp/compose-link-overhaul/owdex.toml.default ./owdex.toml
mv /tmp/compose-link-overhaul/indices.json.default ./indices.json
mv /tmp/compose-link-overhaul/misc/configset /tmp/compose-link-overhaul/misc/entrypoint.sh ./misc
rm -rf /tmp/compose-link-overhaul.zip /tmp/compose-link-overhaul

echo "Setting permissions..."
sudo chown -R 8983 ./data/solr

echo "All done. Happy searching!"

exit

#!/bin/bash

echo "Setting up your Owdex development installation."
echo "This should not be used in production. See https://github.com/owdex/compose."

# cd to script location, just in case
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Creating data folders if they don't exist..."
mkdir -p ./data/solr
mkdir -p ./data/mongo

echo "Purging existing misc files..."
rm -rf ./misc

echo "Creating misc directory..."
mkdir -p ./misc

echo "Downloading configuration files..."
wget "https://github.com/owdex/compose/archive/refs/heads/link-overhaul.zip" -O /tmp/compose-link-overhaul.zip
unzip /tmp/compose-link-overhaul.zip -d /tmp
mv /tmp/compose-link-overhaul/owdex.toml.default ./owdex.toml
mv /tmp/compose-link-overhaul/misc/configset /tmp/compose-link-overhaul/misc/entrypoint.sh ./misc
rm -rf /tmp/compose-link-overhaul.zip /tmp/compose-link-overhaul

echo "Setting permissions..."
sudo chown -R 8983 ./data/solr

echo "All done. Happy searching!"

exit

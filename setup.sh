#!/bin/bash

echo "Setting up your Owdex development installation."
echo "This should not be used in production. See https://github.com/owdex/compose."

# check run as root/sudo
if [ "$EUID" -ne 0 ]
  then echo "Error: This script must be run as root to set permissions."
  exit
fi

# cd to script location, just in case
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Creating data folders if they don't exist..."
mkdir -p ./data/solr
mkdir -p ./data/mongo

echo "Creating misc directory..."
mkdir -p ./misc

echo "Downloading configuration files..."
wget "https://github.com/owdex/compose/archive/refs/heads/main.zip" -O /tmp/compose-main.zip
unzip /tmp/compose-main.zip -d /tmp
mv /tmp/compose-main/owdex.toml .
mv /tmp/compose-main/misc/solr_configset /tmp/compose-main/misc/solr_entrypoint.sh ./misc
# rm -rf /tmp/compose-main.zip /tmp/compose-main

echo "Setting permissions..."
chown -R 8983 ./data/solr

echo "All done. Happy searching!"

exit

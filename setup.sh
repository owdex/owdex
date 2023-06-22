#!/bin/bash

echo "Setting up your Owdex development installation."
echo "This should not be used in production. See https://github.com/owdex/compose."

# cd to script location, just in case
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Checking for prerequisites..."
pre-commit --version > /dev/null || exit 1
npm --version > /dev/null || exit 1
wget --version > /dev/null || exit 1
unzip --help  > /dev/null || exit 1

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
wget -q "https://github.com/owdex/compose/archive/refs/heads/main.zip" -O /tmp/compose-main.zip
unzip -q /tmp/compose-main.zip -d /tmp
mv /tmp/compose-main/owdex.toml.default ./owdex.toml
sed -i 's/debug = false/debug = true/' owdex.toml
mv /tmp/compose-main/misc/configset /tmp/compose-main/misc/entrypoint.sh ./misc
rm -rf /tmp/compose-main.zip /tmp/compose-main

echo "Setting permissions..."
sudo chown -R 8983 ./data/solr

echo "Creating and/or entering venv..."
python3 -m venv .venv
. .venv/bin/activate
pip install -q -r owdex/requirements.txt

echo "All done. Happy searching!"

exit

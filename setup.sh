#!/bin/sh
# owdex setup script for easy configuration. creates the 'data' folders that solr will look for.

if [ "$EUID" -ne 0 ]; then 
    echo "owdex setup should be run as root in order to transfer ownership of the data folder correctly"
    exit
fi

mkdir data data/data data/logs
echo "successfully made folder structure"
chown -R 8983 data 
echo "solr folders now owned by 8983:8983"

echo "done :)"
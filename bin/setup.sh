#!/bin/sh
# owdex setup script for easy configuration

if [ "$EUID" -ne 0 ]; then 
    echo "owdex setup should be run as root in order to transfer ownership of the data folder correctly"
    exit
fi

echo "making data folder structure"
mkdir db/solr/data db/solr/data/data db/solr/data/logs
chown -R 8983 db/solr/data


echo "done :)"

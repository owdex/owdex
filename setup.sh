#!/bin/sh
# owdex setup script for easy configuration

if [ "$EUID" -ne 0 ]; then 
    echo "owdex setup should be run as root in order to transfer ownership of the data folder correctly"
    exit
fi

echo "making data folder structure"
mkdir data data/data data/logs
chown -R 8983 data 


echo "done :)"
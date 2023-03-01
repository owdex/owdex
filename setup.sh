#!/bin/sh
# owdex setup script for easy configuration

if [ "$EUID" -ne 0 ]; then 
    echo "owdex setup should be run as root in order to transfer ownership of the data folder correctly"
    exit
fi

echo "making data folder structure"
mkdir data data/data data/logs
chown -R 8983 data 
echo "initialising solr"
docker-compose up -d solr
sleep 3
docker-compose down
echo "linking solr configuration and schema files"
# obviously, /config/schema.xml doesn't exist on the host.
# it's the mount point for the files in the container as defined by docker-compose.yml
# so these links will be broken on the host but work fine in the container :)
ln -sf /config/schema.xml data/data/stable/conf/schema.xml
ln -sf /config/schema.xml data/data/unstable/conf/schema.xml
ln -sf /config/schema.xml data/data/archive/conf/schema.xml
ln -sf /config/solrconfig.xml data/data/stable/conf/solrconfig.xml
ln -sf /config/solrconfig.xml data/data/unstable/conf/solrconfig.xml
ln -sf /config/solrconfig.xml data/data/archive/conf/solrconfig.xml


echo "done :)"
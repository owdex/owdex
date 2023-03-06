#!/bin/sh

precreate-core stable /owdex_configset
precreate-core unstable /owdex_configset
precreate-core archive /owdex_configset
/opt/solr-9.1.1/bin/solr start -f

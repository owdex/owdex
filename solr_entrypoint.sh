#!/bin/sh

precreate-core stable /owdex_configset
precreate-core unstable /owdex_configset
precreate-core archive /owdex_configset
precreate-core users /owdex_configset_users
/opt/solr-9.1.1/bin/solr start -f

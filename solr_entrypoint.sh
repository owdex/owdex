#!/bin/sh

precreate-core stable /owdex_configset
precreate-core unstable /owdex_configset
precreate-core archive /owdex_configset
solr start

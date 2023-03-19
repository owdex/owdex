# owdex
**_open web index_**

![Website](https://img.shields.io/website?down_color=red&down_message=down&style=flat-square&up_color=green&up_message=up&url=https%3A%2F%2Fowdex.com)
![License](https://img.shields.io/github/license/alexmshepherd/owdex?style=flat-square&color=blue)

![Vulnerability Checks](https://img.shields.io/github/actions/workflow/status/alexmshepherd/owdex/codeql.yml?label=vulnerability%20checks&style=flat-square)
![Chromium HSTS preload](https://img.shields.io/hsts/preload/owdex.com?style=flat-square)
![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade/owdex.com)

![Trans Rights](https://img.shields.io/badge/trans-rights-ff69b4?style=flat-square)

Owdex is an open index of pages from across the web. Instead of crawling through hypertext based
on links, it only indexes pages that its users direct it to. Owdex aims to build a better 
alternative to web search by cutting through the cruft of junk results and bringing focus to real
information.

> **Warning**  
> Owdex is not even working, let alone production-ready. It is not presently usable to fulfill its 
> intended purpose. For that reason, it's not advisable to use it in a production environment. 
> However, I'm making a hard push towards an alpha release soon, which should be ready Eventually 
> (TM). 

## Requirements
_because nobody can spell Prerequisittes_

### For production install
- Docker

### For development
- Python 3.10+
    - [various packages](/frontend/owdex/requirements.txt)
- Tailwind CSS
- Docker

## Installation
Start by `git clone`ing the repo to an arbitrary location. Then run `chmod +x ./bin/setup.sh; sudo ./bin/setup.sh`. 
This creates a `data` directory for Solr to use, fills it with the subdirectories it needs, and 
sets permissions appropriately (this last step is why it has to be run with `sudo`.) 

## Usage
Production users can run `docker-compose up`. This will run the Solr backend and Flask frontend, 
get them talking to each other, and serve a website on port 80. 

Developers can use our magic helper script with `chmod +x ./bin/dev.sh; ./bin/dev.sh`. This runs 
Solr in the background using Docker and starts Tailwind and Flask in development mode, watching the
source files and reloading on changes.

## Contribution
Please see [CONTRIBUTING.md](/.github/CONTRIBUTING.md).

## Acknowledgement
Thanks to [@4censord](https://github.com/4censord) for exceptional help, suppport and words of advice.

## License 
Owdex is licensed under the [GNU AGPL v3](https://github.com/alexmshepherd/owdex/blob/main/LICENSE).

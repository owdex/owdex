# owdex
**_open web index_**

![Website](https://img.shields.io/website?down_color=red&down_message=down&style=for-the-badge&up_color=forestgreen&up_message=up&url=https%3A%2F%2Fowdex.com)
![License](https://img.shields.io/github/license/owdex/owdex?color=blue&style=for-the-badge)
![Trans Rights](https://img.shields.io/badge/trans-rights-blue?style=for-the-badge)

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/owdex/owdex/codeql.yml?color=forestgreen&label=Vulnerability%20checks&logo=github&style=for-the-badge)
![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade/owdex.com?color=forestgreen&logo=mozilla&publish&style=for-the-badge)
![Chromium HSTS preload](https://img.shields.io/hsts/preload/owdex.com?color=yellow&logo=googlechrome&logoColor=white&style=for-the-badge)

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
All You Need Is Docker™. 

## Installation
Start by `git clone`ing the repo to an arbitrary location. Then run `chmod +x ./bin/setup.sh; sudo ./bin/setup.sh`. 
This creates all the necessary files and directories, and sets permissions where it's needed.

## Usage
It's recommended to use `docker-compose`. You must use either `--profile dev` or `--profile prod`. 

## Contribution
Please see [CONTRIBUTING.md](/.github/CONTRIBUTING.md).

## Acknowledgement
Thanks to [@4censord](https://github.com/4censord) for exceptional help, suppport and words of advice.

## License 
Owdex is licensed under the [GNU AGPL v3](https://github.com/alexmshepherd/owdex/blob/main/LICENSE).

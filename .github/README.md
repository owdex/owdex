# owdex
**_an open web index_**

![Website](https://img.shields.io/website?&style=for-the-badge&url=https%3A%2F%2Fowdex.com)
![GitHub Build Status](https://img.shields.io/github/actions/workflow/status/owdex/owdex/build-and-push-image.yml?style=for-the-badge)
![License](https://img.shields.io/github/license/owdex/owdex?color=blue&style=for-the-badge)
![Trans Rights](https://img.shields.io/badge/trans-rights-blue?style=for-the-badge)

![GitHub Check Status](https://img.shields.io/github/actions/workflow/status/owdex/owdex/codeql.yml?label=Vulnerability%20checks&logo=github&style=for-the-badge)
![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade/owdex.com?logo=mozilla&publish&style=for-the-badge)
![Chromium HSTS preload](https://img.shields.io/hsts/preload/owdex.com?logo=googlechrome&logoColor=white&style=for-the-badge)

Owdex is an open index of pages from across the web. Instead of crawling through hypertext based
on links, it only indexes pages that its users direct it to. Owdex aims to build a better 
alternative to web search by cutting through the cruft of junk results and bringing focus to real
information.

> **Warning**  
> Owdex fulfills minimal specifications. However, most planned features are not yet implemented,
> and it is currently operating on a bleeding-edge release cycle. It may not be advisable to
> use it in a production environment. A more stable, more complete alpha release will be available
> soon. 


## Installation and usage
### For production
For production, we recommend using `docker compose`. You can find a recommended setup, along with 
usage instructions, at [`owdex/compose`](https://github.com/owdex/compose).

### For development
Just `git clone` this repo and run `docker compose up -d`. You can access the frontend at 
[`http://127.0.0.1`](http://127.0.0.1). After making any changes to the frontend, just run 
`docker compose restart frontend` to selectively restart it.

## Contribution
Please see [CONTRIBUTING.md](/.github/CONTRIBUTING.md).

## Acknowledgement
Thanks to [@4censord](https://github.com/4censord) for exceptional help, suppport and words of advice.

## License 
Owdex is licensed under the [GNU AGPL v3](https://github.com/alexmshepherd/owdex/blob/main/LICENSE).

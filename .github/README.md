# owdex

![Release number](https://img.shields.io/github/v/release/owdex/owdex?style=for-the-badge)
![License](https://img.shields.io/github/license/owdex/owdex?color=blue&style=for-the-badge)
![Trans Rights](https://img.shields.io/badge/trans-rights-blue?style=for-the-badge)

![GitHub Build Status](https://img.shields.io/github/actions/workflow/status/owdex/owdex/build-and-push.yml?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Check Status](https://img.shields.io/github/actions/workflow/status/owdex/owdex/codeql.yml?label=Vulnerability%20checks&logo=github&style=for-the-badge)

![Website](https://img.shields.io/website?&style=for-the-badge&url=https%3A%2F%2Fowdex.com)
![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade/owdex.com?logo=mozilla&publish&style=for-the-badge)
![Chromium HSTS preload](https://img.shields.io/hsts/preload/owdex.com?logo=googlechrome&logoColor=white&style=for-the-badge)

## **_an open web index_**

Owdex is an open index of pages from across the web. Instead of crawling through hypertext based on links, it only indexes pages that its users direct it to. Owdex aims to build a better alternative to web search by cutting through the cruft of junk results and bringing focus to real information.

## Installation and usage
### In production
#### With Docker Compose (recommended)
We recommend using Docker Compose in production. An example setup is available at [**`owdex/compose`**](https://github.com/owdex/compose).

```shell
$ git clone https://github.com/owdex/compose.git owdex && cd owdex
$ chmod +x setup.sh
$ ./setup.sh
$ nano owdex.toml
# Edit the configuration file, being sure to change the secret key and admin password.
$ nano misc/Caddyfile
# Edit the reverse proxy configuration, being sure to change the domain name and email.
$ docker compose up -d
```

#### With Docker
If you already have Solr and MongoDB instances running elsewhere, you can just use Owdex on its own. Images are available for every release from the [GitHub Container Registry](https://github.com/orgs/owdex/packages/container/package/owdex). 

```shell
$ wget https://raw.githubusercontent.com/owdex/compose/main/owdex.toml.default -O owdex.toml
$ nano owdex.toml
# Edit the configuration file, being sure to change the secret key, admin password and database hostnames.
$ docker run --detach --volume ./owdex.toml:/owdex.toml:ro  ghcr.io/owdex/owdex:main
```

### In development
You'll still likely want to use Docker Compose, as it makes managing the databases, as well as building Tailwind CSS, no longer your problem.

```shell
$ git clone https://github.com/owdex/owdex.git
$ chmod +x setup.sh
$ ./setup.sh
$ docker compose up --build -d
```

While you can make changes to `owdex.toml`, you don't necessarily have to change the admin password or secret key, as these don't matter much in a non-exposed development environment. You can then access the frontend at [`http://127.0.0.1`](http://127.0.0.1).

## Contribution
Please see [CONTRIBUTING.md](/.github/CONTRIBUTING.md).

## Acknowledgement
Thanks to [@4censord](https://github.com/4censord) for exceptional help, suppport and words of advice.

## License 
Owdex is licensed under the [GNU AGPL v3](https://github.com/alexmshepherd/owdex/blob/main/LICENSE).

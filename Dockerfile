# Version of Dart-Sass to use
ARG UPSTREAM_VERSION=1.62.1

# Some code here taken from https://github.com/michalklempa/docker-dart-sass
FROM alpine:3 as scss_build
ARG UPSTREAM_VERSION
ADD https://github.com/sass/dart-sass/releases/download/${UPSTREAM_VERSION}/dart-sass-${UPSTREAM_VERSION}-linux-x64.tar.gz /opt/
RUN tar -C /opt/ -xzvf /opt/dart-sass-${UPSTREAM_VERSION}-linux-x64.tar.gz
WORKDIR /scss
COPY owdex/static/scss .
RUN /opt/dart-sass/sass --style=compressed main.scss /build.css

FROM python:3-alpine AS flask
WORKDIR /build
COPY owdex/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=scss_build /build.css owdex/static/build.css
COPY . .
CMD [ "python", "-m", "owdex" ]

LABEL org.opencontainers.image.source = "https://github.com/owdex/owdex"
LABEL org.opencontainers.image.title = "Owdex frontend"

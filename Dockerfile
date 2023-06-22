# Build SCSS to CSS
    FROM dart:stable AS scss_build
    COPY --from=bufbuild/buf /usr/local/bin/buf /usr/local/bin/

    WORKDIR /dart-sass
    RUN git clone https://github.com/sass/dart-sass.git . && \
        dart pub get && \
        dart run grinder protobuf

    COPY owdex/static/scss /scss
    RUN dart ./bin/sass.dart /scss/main.scss /build.css


# Run Flask webapp
    FROM python:3-alpine AS flask
    WORKDIR /build

    COPY owdex/requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY --from=scss_build /build.css owdex/static/build.css

    COPY . .
    CMD [ "python", "-m", "owdex" ]


# Metadata
    LABEL org.opencontainers.image.source = "https://github.com/owdex/owdex"
    LABEL org.opencontainers.image.title = "Owdex frontend"

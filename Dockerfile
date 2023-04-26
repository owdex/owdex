FROM python:3-alpine AS flask_build
WORKDIR /build
COPY owdex/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "-m", "owdex" ]

LABEL org.opencontainers.image.source = "https://github.com/owdex/owdex"
LABEL org.opencontainers.image.title = "Owdex frontend"

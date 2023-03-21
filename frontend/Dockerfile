FROM node:19-alpine AS tailwind_build
WORKDIR /build_css
RUN npm install tailwindcss
COPY . .
RUN npx tailwindcss -o /build.css --minify


FROM python:3-alpine AS flask_build
WORKDIR /build
COPY . .
RUN pip install --no-cache-dir -r owdex/requirements.txt
COPY --from=tailwind_build /build.css owdex/static/tailwind.css
CMD [ "python", "-m", "owdex" ]

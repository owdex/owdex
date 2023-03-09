FROM python:3-alpine

WORKDIR /build

COPY . .

RUN pip install --no-cache-dir -r owdex/requirements.txt

CMD [ "python", "-m", "owdex" ]

# which starter docker image to work with
FROM python:3.10-slim

# choose working dir
WORKDIR /app

COPY pyproject.toml .

COPY court_scraper/ court_scraper/

COPY entrypoint.sh ./entrypoint.sh

RUN pip install --no-cache-dir .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
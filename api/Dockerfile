FROM python:3.9-slim-buster
LABEL maintainer="Sibylline - ben@sibylline.xyz"

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get -qq update && \
    apt-get install --no-install-recommends -y -qq gcc python3-pip libpq-dev python3-dev  \
    default-libmysqlclient-dev build-essential ca-certificates automake libtool make pkg-config && \
    pip3 install -r requirements.txt

RUN python -c "import tiktoken; tiktoken.encoding_for_model('gpt-4')"
RUN python -m nltk.downloader punkt

COPY . ./

USER 1005

ENTRYPOINT ["uvicorn", "api.main:app", "--loop", "asyncio", "--host", "0.0.0.0", "--workers", "5"]
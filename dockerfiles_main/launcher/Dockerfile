FROM docker:23.0.0-beta.1-cli-alpine3.17
WORKDIR /
COPY requirements.txt /
RUN apk add --no-cache python3 py3-pip
RUN pip install -r requirements.txt
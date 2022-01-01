FROM python:3.9-alpine3.12
RUN addgroup -S swuser  && adduser -S swuser -G swuser
RUN mkdir /bbot
WORKDIR /bbot
COPY requirements.txt /bbot
RUN pip install --upgrade pip
RUN apk add --update --no-cache g++ libxslt-dev gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN pip install -r requirements.txt
RUN apk del g++ libxslt-dev gcc musl-dev python3-dev libffi-dev openssl-dev cargo
COPY . /bbot
USER swuser
CMD [ "python", "./blab.py" ]

FROM python:3.8-slim-buster
RUN groupadd deploy && useradd -g deploy deploy

COPY . /app

RUN apt-get update -qq && apt-get install gcc openssh-client git -y

WORKDIR /app
ENV PYTHONPATH /app
RUN pip3 install --upgrade pip && pip3 install flake8
#RUN flake8 .
RUN pip3 install -r requirements.txt
RUN chmod +x run.sh

ENTRYPOINT ["/app/run.sh"]

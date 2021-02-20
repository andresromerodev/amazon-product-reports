FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip

RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py"]

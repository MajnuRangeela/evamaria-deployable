FROM python:3.10-slim-buster

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt -qq update --fix-missing
RUN apt install git -y

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get upgrade -y

CMD ["bash", "start.sh"]
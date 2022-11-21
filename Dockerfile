FROM ubuntu
WORKDIR /code
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y libsndfile1
RUN python3 -m pip install -U pip
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
ENV TZ=Europe/London
ENV DEBIAN_FRONTEND=noninteractive
EXPOSE 5544
COPY . .
CMD ["python3", "-u", "./app.py"]

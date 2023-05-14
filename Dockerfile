FROM python:3.8-slim

WORKDIR /object_counter

ADD . /object_counter

RUN pip3 install -r requirements.txt

CMD ["python","-u", "-m", "counter.entrypoints.webapp"]

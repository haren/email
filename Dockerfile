FROM python:2.7

COPY . /app/
WORKDIR /app/
RUN pip install -r server/requirements
CMD python server/server.py
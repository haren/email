# Requiered: docker

# docker build -t server .
# docker run --net="host" -d redis
# docker run --net="host" -d server


FROM python:2.7

COPY . /app/
WORKDIR /app/
RUN pip install -r requirements
CMD python server/server.py
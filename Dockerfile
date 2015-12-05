# Requiered: docker

# docker build -t server .
# docker run --net="host" -d redis
# docker run --net="host" -v REPO_PATH/server/logs:/app/server/logs -d server


FROM python:2.7

COPY . /app/
WORKDIR /app/
RUN pip install -r server/requirements
CMD python server/server.py
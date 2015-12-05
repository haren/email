FROM python:2.7

COPY . /app/
WORKDIR /app/
RUN pip install -r requirements
EXPOSE 80
CMD python server/server.py
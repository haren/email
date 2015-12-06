# Web Email Sending Service Server

This directory contains the backend part of the project.

## Installation and Requirements
The project can be installed on any UNIX system. The only external requirement is `docker`. Installation instructions can be found [here](http://docs.docker.com/engine/installation/). 

Mac OS requires also a docker porting solution, such as [`docker machine`](https://docs.docker.com/machine/) (recommended) or [`boot2docker`](http://boot2docker.io/)

**The solution has been deployed and tested on `OS X El Captain 10.11.1` and `Amazon Ubuntu Server 14.04`.**

## Running the server
To prepare the server to run, docker images need to be built (or pulled from docker hub) with the following commands:

```
# build server image
docker build -t server .            

# start redis container (and pull from hub if necessary)
docker run --net="host" -d redis    

# start server container and map the logs dir to host
# IMPORTANT: replace REPO_PATH with the absolute path to your main repo directory,
# AND YOUR_ACCESS_KEY and YOUR_SECRET_ACCESS_KEY with your AWS credentials.
docker run --net="host" \
	-v REPO_PATH/server/logs:/app/server/logs \
	-e AWS_ACCESS_KEY_ID='YOUR_ACCESS_KEY' \
	-e AWS_SECRET_ACCESS_KEY='YOUR_SECRET_ACCESS_KEY' \
	-d server
```

## Shutting down the server
To shut down the server, simply stop the docker container in which the server process (`python server.py`) is running:

```
# search for the container id
docker ps

# stop the container
docker stop SERVER_CONTAIENR_ID
```

## Usage

### Response Format

All the responses are returned in `JSON` format (except for serving the web page). Sample response is presented below. Response always returns HTML code `200` and the status indicates request handling effect.

 - `status` is an integer number,
 - `send_status` is a string indicating the requested email send status.
```
{"status": 200, "send_status": "SENT"}
```

### Routing

| Path | Description |
|----|----|
| `/emails/` | GET lists all emails a given user (cookie-identified) has sent, POST sends an email. |
| `/delivered/mailgun/` | POST servers as a handler for a delivery webhook confirmation for Mailgun service. |
| `/delivered/ses/` | POST servers as a handler for a delivery webhook confirmation for AWS SES service. |
| `/rejected/mailgun/` | POST servers as a handler for a rejection webhook for Mailgun service. |
| `/rejected/ses/` | POST servers as a handler for a rejection webhook for AWS SES service. |
| `/` | GET servers the web app. |


All other requests will results in the following response

```
{"status": 404, "msg": "Incorrect request url."}
```

### Configuration

All necessary configuration changes can be performed in the `config.py` file. The constans are self-explanatory.

**IMPORTANT:** Application requires you to register your own accounts with each external email sending providers. The provided API keys should be then placed into `config.py` file. Keys for AWS SES service should be put in a [boto-accessible file](http://boto.cloudhackers.com/en/latest/boto_config_tut.html), e.g. `~/.aws/credentials`.

### Logging

The application logs all important events into a time-rotating log file. The log file is structured as follows:
```
/server/logs/main.log/main.log
```
And is created automatically upon server start.

## Testing

Test suite has been prepared for the app. To run the test suite, make sure the test is running and perform the following:

```
cd servers/test
python run_tests.py
```

The test process exists with an appropriate exit code so that it can be directly plugged into an e.g. continuous integration solution.

**IMPORTANT** : When executing tests, make sure that the IP address under which the test suite sees the server is correct. This can be configured in `config.py` (`HOST` constant).

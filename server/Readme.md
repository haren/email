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
# IMPORTANT: replace REPO_PATH with the absolute path to your main repo directory
docker run --net="host" -v REPO_PATH/server/logs:/app/server/logs -d server
```

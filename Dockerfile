FROM ubuntu:latest

#Use /bin/bash as default shell
SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

# create share folder
RUN mkdir -p /root/share

# install dependencies:
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y curl git-core python3-pip

# install latest node.js 10.x
RUN curl -o /tmp/add.sh https://deb.nodesource.com/setup_10.x
RUN /bin/bash /tmp/add.sh
RUN apt install -y nodejs

# install gulp
RUN npm install -g gulp-cli

# get ct-online repository
RUN git clone https://github.com/ct-online/cto.git /root/cto

# set workdir to /root
WORKDIR /root
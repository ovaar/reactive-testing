FROM ubuntu:20.04

# Bash "strict mode"
# RUN set -euo pipefail

# Update the package listing
RUN apt-get update

# Install security updates
RUN apt-get -y upgrade

# Install Python 3.8
RUN apt-get install -y python3.8 python3-pip

# Set default python executable to 3.8
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

RUN python --version
RUN pip3 --version

RUN apt-get install -y mosquitto mosquitto-clients

# Delete cached files
RUN apt-get clean

# Install requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Add sources
WORKDIR /lighting/base
ADD src/ src
ADD __init__.py .
RUN touch /lighting/__init__.py

# Set environment variables
ENV PYTHONPATH=/
ENV PYTHONUNBUFFERED=1

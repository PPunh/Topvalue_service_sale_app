# Use python 3.12 on Debain 12 bookworm
FROM python:3.12-bookworm
LABEL maintainer="Mong, mr.souriya@gmail.com, PITEC.la"

ENV PYTHONUNBUFFERED=1

# Copy requirement file to tmp directory
COPY ./requirements/production.txt /tmp/production.txt
COPY ./requirements/development.txt /tmp/development.txt

# Copy django project files from django-project on host to django-project directory on docker
# COPY ./django-project /django-project

# Set working directory
WORKDIR /django-project

# Expose port
# django for cpserver (production)
EXPOSE 8000
# django for runserver (development purpose)
EXPOSE 8001
# pgAdmin
EXPOSE 5050

# Set the DEBIAN_FRONTEND environment variable to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Set timezone for the base OS image
ENV TZ=Asia/Vientiane
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

# Set valuable to be use to determine Development or Production
ARG DEV=false

# Update system
# libpq5, build-essential are dependencies for psycopg3 in requirements file
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils libpq5 build-essential memcached openssl && \
    apt-get upgrade -y && \
    apt-get autoremove -y

# Install dependencies for installing psycopg3
# RUN apt-get install -y libpq5 build-essential

# Create python virtual environment
RUN python3 -m venv /venv

# Upgrade pip and install install requirements
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r /tmp/production.txt

# Install additional requirements for development if DEV is true, set this value in compose file
RUN if [ $DEV = "true" ]; then /venv/bin/pip install -r /tmp/development.txt; fi

# Install django-filter lib explicitly, due to containerize limitation
# if having issues when install this lib using requirements file
# RUN /venv/bin/pip install django-filter

# Remove temporary files
RUN rm -rf /tmp

# Create user account to run django app
RUN adduser --disabled-password --no-create-home django-user

# Set default path to the virtual env directory
ENV PATH="/venv/bin:$PATH"

# Switch to django-user
USER django-user

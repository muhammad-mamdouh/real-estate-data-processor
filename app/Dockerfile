# Base upon Python 3.7 image
FROM python:3.7
LABEL maintainer="mahammad.mamdouh@gmail.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
ENV HOME=/app
WORKDIR /app/realestate_module

# Install environment dependencies
COPY ./requirements/base.txt .
RUN pip3 install --upgrade pip \
    && pip3 install -r base.txt

## Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add the current working directory code to the container's working directory
ADD . .

# Creating app user and switch to it
RUN useradd app_user \
    && chown -R app_user:app_user $HOME

# Copy and run the entrypoint script
COPY ./entrypoint.sh .
RUN chmod 755 entrypoint.sh
ENTRYPOINT ["sh", "/app/realestate_module/entrypoint.sh"]

# Switch to ach user
USER app_user

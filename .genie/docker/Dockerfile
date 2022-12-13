FROM ubuntu:20.04

# Environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ="Asia/Kolkata"
ENV PATH="/home/user/.local/bin:$PATH"


# Setup working directory
RUN mkdir /app
COPY ./project /app

# Update the system
RUN apt-get update -y
RUN apt-get install -y sqlite

# Install python and pip
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Essential directories and files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Run the app
RUN cd /app
WORKDIR /app

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

CMD [ "python","manage.py","runserver", "0.0.0.0:8000" ]

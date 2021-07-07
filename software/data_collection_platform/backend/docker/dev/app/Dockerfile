FROM python:3.8.5
LABEL maintainer="er.li@mail.mcgill.ca"

# run python in unbuffered mode which is recommended when running Docker in containers (doesn't allow Python to buffer the output, instead prints them directly to avoid log being stucked in buffer when container is closed)
ENV PYTHONUNBUFFERED 1 
# prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 

# add scripts to the path of the running container  
ENV PATH="/scripts:${PATH}"

# Set the working directory.
WORKDIR /usr/src/dcp/backend

# copy app to container 
COPY . /usr/src/dcp/backend

# activate environment
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# install netcat
RUN apt-get update && apt-get -y install netcat

# copy entrypoint file
COPY ./docker/dev/app/entrypoint.sh /scripts/entrypoint.sh

# give executable permission to all scripts
RUN chmod +x /scripts/*

ENTRYPOINT [ "entrypoint.sh" ]

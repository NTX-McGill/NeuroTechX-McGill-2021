FROM python:3.8.5
LABEL maintainer="er.li@mail.mcgill.ca"

# run python in unbuffered mode which is recommended when running Docker in containers (doesn't allow Python to buffer the output, instead prints them directly to avoid log being stucked in buffer when container is closed)
ENV PYTHONUNBUFFERED 1 
# prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 

# Set the working directory.
WORKDIR /usr/src/dcp/backend/OpenBCI_GUI/Networking-Test-Kit/LSL

# activate environment
RUN pip install --upgrade pip
RUN pip install pylsl

SHELL ["/bin/bash", "-c"]

# use `docker-compose -f docker-compose.test.yml build` 
# then `docker-compose -f docker-compose.test.yml run app bash`
#! /bin/bash

# starting a celery worker
celery -A celery worker --loglevel=info
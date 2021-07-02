#! /bin/bash

# starting a celery worker
celery -A dcp.celery worker --loglevel=info
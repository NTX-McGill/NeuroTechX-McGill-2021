#!/bin/sh

# starting a celery worker
celery -A dcp.run_celery.celery worker --loglevel=info

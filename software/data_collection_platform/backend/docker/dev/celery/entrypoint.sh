#!/bin/bash

echo "Starting celery task workers."
celery -A dcp.run_celery.celery worker --loglevel=info
echo "Celery task workers started."

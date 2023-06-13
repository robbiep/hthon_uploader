#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=development

# Set the desired values for these variables
export DATA_DIR="~/data/training"

# Activate your virtual environment if necessary
# source /path/to/venv/bin/activate

flask run --host=127.0.0.1 --port=5000

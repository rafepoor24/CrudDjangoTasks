#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requiremens.txt
python manage.py collectstatic --no-input
python manage.py migrate
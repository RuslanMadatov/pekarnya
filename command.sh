#!/usr/bin/env bash


source venv/bin/activate
python manage.py runserver --settings=pshop.settings_dev

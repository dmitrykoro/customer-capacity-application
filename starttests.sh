#!/bin/bash

source venv/bin/activate

coverage run --source=src/dbapi -m unittest -v
coverage report


#!/bin/bash


set -e

./scripts/check_migrations.sh

pytest "${@:-pyorc}"

flake8 pyorc fabfile.py

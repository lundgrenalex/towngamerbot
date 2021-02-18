#!/bin/sh

# Активировать окружение

export PYTHONPATH=$PYTHONPATH:$(pwd)
. .env/bin/activate

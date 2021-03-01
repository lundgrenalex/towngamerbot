#!/usr/bin/env bash

set -e

python3 ./migrations/mongo.py && python3 src/app/bot.py

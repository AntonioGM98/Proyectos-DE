#!/bin/bash

ENV=$1

function USAGE() {
  echo "USAGE: ./run-local.sh" &>/dev/stderr
  exit 1
}

PYTHONPATH=app uvicorn main:app --port 8000 --reload

#!/usr/bin/env bash

while true; do
  echo "yes" | python src/manage.py collectstatic
  echo "Sleeping for 1 second"
  sleep 1
done


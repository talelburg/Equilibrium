#!/bin/bash

if [ "$1" == "clean" ]; then
  echo "Removing data"
  rm -rf data
  echo "Removing logs"
  rm -rf logs
fi

echo "Down"
docker-compose down
echo "Build"
docker-compose build
echo "Up"
docker-compose up
echo "Done"
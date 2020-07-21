#!/bin/bash
set -x
echo "stopping services.. "
docker-compose stop
echo "Removing serving.. "
docker-compose rm -f
echo "Removing any dangling images.."
docker rmi -f $(docker images -qf dangling=true)


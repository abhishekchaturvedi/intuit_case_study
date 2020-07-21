#!/bin/bash
set -x
echo "Resetting the db and creating an admin user"
docker-compose exec userlogin_app userlogin db reset


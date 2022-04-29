#!/usr/bin/bash

export FLASK_APP=martha
export FLASK_ENV=devolopment
export DB_PASSWORD=<db_:qpassword>
export DB_USERNAME=<db_user>
flask run --host=0.0.0.0


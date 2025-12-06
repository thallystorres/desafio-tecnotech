#!/bin/sh

set -e

wait_psql.sh
migrate.sh
run_tests.sh
runserver.sh

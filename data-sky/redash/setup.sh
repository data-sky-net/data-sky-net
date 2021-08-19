#!/usr/bin/env bash
# This script setups dockerized Redash on Ubuntu 18.04.
set -eu

REDASH_BASE_PATH=/opt/redash

create_directories() {
    if [[ ! -e $REDASH_BASE_PATH ]]; then
        sudo mkdir -p $REDASH_BASE_PATH
        sudo chown $USER:$USER $REDASH_BASE_PATH
    fi

    if [[ ! -e $REDASH_BASE_PATH/postgres-data ]]; then
        mkdir $REDASH_BASE_PATH/postgres-data
    fi
}

create_config() {
    if [[ -e $REDASH_BASE_PATH/env ]]; then
        rm $REDASH_BASE_PATH/env
        touch $REDASH_BASE_PATH/env
    fi

    COOKIE_SECRET=jx0TnY0ZWkvpqwmADwfo80MGUbbvR1dj
    SECRET_KEY=pkKbQCPWA1iUbzeARELJ23wkYmFHg6FN
    POSTGRES_PASSWORD=mhgyguy3ydKrEkShOqigtaldzEOmWWoM
    REDASH_DATABASE_URL="postgresql://postgres:${POSTGRES_PASSWORD}@postgres/postgres"

    echo "PYTHONUNBUFFERED=0" >> $REDASH_BASE_PATH/env
    echo "REDASH_LOG_LEVEL=INFO" >> $REDASH_BASE_PATH/env
    echo "REDASH_REDIS_URL=redis://redis:6379/0" >> $REDASH_BASE_PATH/env
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> $REDASH_BASE_PATH/env
    echo "REDASH_COOKIE_SECRET=$COOKIE_SECRET" >> $REDASH_BASE_PATH/env
    echo "REDASH_SECRET_KEY=$SECRET_KEY" >> $REDASH_BASE_PATH/env
    echo "REDASH_DATABASE_URL=$REDASH_DATABASE_URL" >> $REDASH_BASE_PATH/env
}

setup_compose() {
    REQUESTED_CHANNEL=stable
    LATEST_VERSION=`curl -s "https://version.redash.io/api/releases?channel=$REQUESTED_CHANNEL"  | json_pp  | grep "docker_image" | head -n 1 | awk 'BEGIN{FS=":"}{print $3}' | awk 'BEGIN{FS="\""}{print $1}'`

    cp ${PWD%/ds_project_deploy_wizard/*}/ds_project_deploy_wizard/data-sky/redash/docker-compose.yml $REDASH_BASE_PATH/
    COMPOSE_FILE=/opt/redash/docker-compose.yml
    sudo docker-compose -f $COMPOSE_FILE -p redash run --rm server create_db
    sudo docker-compose -f $COMPOSE_FILE -p redash up -d
}

create_directories
create_config
setup_compose

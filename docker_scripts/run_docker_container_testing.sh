#!/usr/bin/env bash

show_help(){
    echo "Usage: ./run_docker_contatiner_testing.sh -t IMAGE_TAG"
}

TAG="unittests"
while getopts "h?t:" opt; do
    case "$opt" in
        h|\?)   show_help ; exit 0 ;;
        t)      TAG="$OPTARG" ;;
    esac
done

docker run --rm ds_project_deploy_wizard:$TAG

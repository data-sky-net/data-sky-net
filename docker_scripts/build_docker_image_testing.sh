#!/usr/bin/env bash

show_help(){
    echo "Usage: ./build_docker_image_testing.sh -t IMAGE_TAG"
}

TAG="unittests"
while getopts "h?t:" opt; do
    case "$opt" in
        h|\?)   show_help ; exit 0 ;;
        t)      TAG="$OPTARG" ;;
    esac
done

PYTHON_VERSION=$(cat .python-version)
docker build -t ds_project_deploy_wizard:$TAG -f dockerfiles/Dockerfile_testing --build-arg PYTHON_VERSION=${PYTHON_VERSION} .

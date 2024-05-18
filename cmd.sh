#!/usr/bin/env bash
set -x #echo on

BASEDIR=$(dirname "$0")
DOCKERDIR=$BASEDIR/docker
PLATFORM=linux/amd64
REGISTRY=ttl.sh

echo "BASEDIR: $BASEDIR"
echo "DOCKERDIR: $DOCKERDIR"

case "$1" in
  "dockerize:api")
    echo "Building Docker image for API..."
    docker buildx build --platform $PLATFORM -t $2 -f $DOCKERDIR/Dockerfile.api $BASEDIR
    ;;
  "dockerize:bot")
    echo "Building Docker image for Bot..."
    docker buildx build --platform $PLATFORM -t $2 -f $DOCKERDIR/Dockerfile.bot $BASEDIR
    ;;
  "docker:publish")
    echo "Publishing Docker image..."
    docker push $2
    ;;
  *)
    echo "Usage: $0 {dockerize:api|dockerize:bot|docker:publish}"
    exit 1
    ;;
esac

exit 0

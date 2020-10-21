#!/bin/bash
REPO_NAME=$1
MODULE_ROOT_PATH=" src/${REPO_NAME}"
TMP_GEN_PATH="tmp/python-flask"
API_DEF_PATH="$TMP_GEN_PATH/${REPO_NAME}_api"
API_FILENAME="${REPO_NAME}_api.yaml"

GENERATOR_PATH="openapi_generator"
GENERATOR_JAR="$GENERATOR_PATH/openapi-generator-cli.jar"

JAVA_OPTS=""
CLASS_PATH="-cp .:-/src"

export PYTHON_POST_PROCESS_FILE="/usr/local/bin/yapf -i"

echo "Generating ${SENSOR_NAME}"
rm -Rf $API_DEF_PATH
VERSION=`java $JAVA_OPTS $CLASS_PATH -jar $GENERATOR_JAR version`
echo "Using version $VERSION"
java $JAVA_OPTS $CLASS_PATH -jar $GENERATOR_JAR generate \
  -i $MODULE_ROOT_PATH/api_def/$API_FILENAME \
  -g python-flask \
  -o $API_DEF_PATH

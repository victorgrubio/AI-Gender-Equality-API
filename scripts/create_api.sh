#!/bin/sh
REPO_NAME="gender_equality"
MODULE_ROOT_PATH="src/${REPO_NAME}"
TMP_GEN_PATH="tmp/python-flask/${REPO_NAME}_api"
API_DEF_PATH="$TMP_GEN_PATH/openapi_server"

export PYTHON_POST_PROCESS_FILE="/usr/local/bin/yapf -i"

# Clear module path before creating new modules
rm -Rf $MODULE_ROOT_PATH/modules/

./scripts/make_server.sh $REPO_NAME

if [ -f $API_DEF_PATH/openapi/openapi.yaml ]; then
    echo "Copying openapi_server to ${REPO_NAME} source"
    #rm -Rf $MODULE_ROOT_PATH/openapi/openapi.yaml
    #mkdir -p $MODULE_ROOT_PATH/openapi
    #cp $API_DEF_PATH/openapi/openapi.yaml $MODULE_ROOT_PATH/openapi/openapi.yaml
    cp -Rf $API_DEF_PATH/* $MODULE_ROOT_PATH/openapi_server
fi

#!/bin/bash
export ARTIFACT_REGISTRY_TOKEN=$(gcloud auth print-access-token)
export UV_PUBLISH_USERNAME=oauth2accesstoken
export UV_PUBLISH_PASSWORD="$ARTIFACT_REGISTRY_TOKEN"

rm -fr dist
uv build
uv publish --index pypi-gc

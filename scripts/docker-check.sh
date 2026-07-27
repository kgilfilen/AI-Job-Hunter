#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="ai-job-hunter"
TEST_MODE="${1:-unit}"

docker build -t "$IMAGE_NAME" .

case "$TEST_MODE" in
    unit)
        docker run --rm "$IMAGE_NAME" \
            python -m pytest tests/unit -v
        ;;

    integration)
        docker run --rm \
            --env-file .env \
            "$IMAGE_NAME" \
            python -m pytest tests/integration -v
        ;;

    all)
        docker run --rm \
            --env-file .env \
            "$IMAGE_NAME" \
            python -m pytest -v
        ;;

    *)
        echo "Usage: $0 [unit|integration|all]"
        exit 1
        ;;
esac
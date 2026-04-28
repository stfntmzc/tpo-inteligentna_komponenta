#!/usr/bin/env bash

API_URL="${1:-http://127.0.0.1:12000/api/moderate}"
IMAGE_DIR="${2:-test/images}"

echo "Testing images from: $IMAGE_DIR"
echo "API endpoint: $API_URL"
echo "============================================================"

if [ ! -d "$IMAGE_DIR" ]; then
    echo "Error: image directory does not exist: $IMAGE_DIR"
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "Error: jq is not installed."
    echo "Install it with: sudo apt install jq"
    exit 1
fi

for image in "$IMAGE_DIR"/*; do
    if [ -f "$image" ]; then
        tmp_file=$(mktemp)

        http_status=$(curl -s -o "$tmp_file" -w "%{http_code}" \
            -X POST "$API_URL" \
            -F "file=@$image")

        echo ""
        echo "Image: $image"
        echo "HTTP status: $http_status"
        echo "Response:"
        jq . "$tmp_file"

        rm "$tmp_file"

        echo ""

        echo "------------------------------------------------------------"
    fi
done
#!/bin/bash

# Helper script to run the Notion date copier

# Check if NOTION_API_KEY is set
if [ -z "$NOTION_API_KEY" ]; then
    echo "Error: NOTION_API_KEY environment variable is not set."
    echo ""
    echo "Please set it first:"
    echo "  export NOTION_API_KEY='your_api_key_here'"
    echo ""
    echo "Then run this script again:"
    echo "  ./run.sh"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Python script using the virtual environment
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/copy_created_dates.py"


#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Error: Please provide the name of the subdirectory under src."
  exit 1
fi

subdirectory="$1"
directory="src/$subdirectory"

# Create the subdirectory inside the src directory if it doesn't exist
mkdir -p "$directory"

# Create each of the files inside the subdirectory
cat << EOF > "$directory/constants.py"
# constants.py
# This is the constants module.
# module specific constants and error codes go here
EOF

cat << EOF > "$directory/dependencies.py"
# dependencies.py
# This is the dependencies module. https://fastapi.tiangolo.com/tutorial/dependencies/
EOF

cat << EOF > "$directory/exceptions.py"
# exceptions.py
# This is the exceptions module.
# module specific exceptions, e.g. PostNotFound, ItemAlreadyExists, etc. go here
EOF

cat << EOF > "$directory/models.py"
# models.py
# Pydantic models go here (not DB models) 
EOF

cat << EOF > "$directory/router.py"
# router.py
# Defining the API endpoints go here and calling the service layer
EOF

cat << EOF > "$directory/schemas.py"
# schemas.py
# DB logic goes here
EOF

cat << EOF > "$directory/service.py"
# service.py
# Module specific business logic goes here
EOF

cat << EOF > "$directory/utils.py"
# utils.py
# Non-business logic related utility functions go here (e.g. hashing, etc.)
# Helper functions that are used in the service layer go here
EOF

echo "Files created successfully in the $subdirectory directory under src."

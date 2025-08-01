# Default recipe - list available commands
default SESSION_NAME="private-facts-fastapi":
    @just --list

# Run app
run:
    uv run fastapi dev src/api/main.py

# Run tests
test *args:
    uv run pytest {{ args }}

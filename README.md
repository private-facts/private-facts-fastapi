# Private Facts FastAPI

This app demonstrates how you can use FastAPI to store data to, and retrieve it from, a Tahoe server.

## Installation
Install dependencies:
```bash
uv sync
```
Create a `.env`:
```bash
cp env-template .env
```

## Running the app
```bash
uv run fastapi dev src/api/main.py
```
or
```bash
just run
```

Once the FastAPI server is running, navigate to `http://127.0.0.1:8000` in a web browser to view the web interface.

To store and retrieve data via the web interface, you will need to be running your own Tahoe storage server and client locally. The app is configured to send requests to port 3456, which is the default port Tahoe listens on. The easiest way to get Tahoe up and running is by cloning the [private-facts](https://github.com/private-facts/private-facts) repo and running `just dev` from within the `private-facts` directory.  

## Running the tests
```bash
uv run pytest
```
or
```bash
just test
```
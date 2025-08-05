# Private Facts FastAPI
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

## Running the tests
```bash
uv run pytest
```
or
```bash
just test
```

### Use case  
This proof-of-concept will
Get a file
    - https://tahoe-lafs.readthedocs.io/en/latest/frontends/webapi.html#reading-a-file


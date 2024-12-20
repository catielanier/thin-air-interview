# Catie Lanier - Thin Air Labs Technical Interview

This is my solution to the technical interview for Thin Air Labs, using Python + Flask with static typings on the backend, and Svelte + Typescript on the frontend. Frontend testing handled by Vitest, Python testing handled by unittest.

## Required technologies

- Python >= 3.12
- Node.js >= 18.20
- Yarn >= 1.22

## Initializing backend

Please input the following commands in the project root directory:

- `python -m venv env`
- `source env/bin/activate`
- `pip install -r Requirements.txt`
- `python server.py`

**NOTE:** If you have installed Python v3 but are receiving an error in terminal that states `command not found`, replace `python` with `python3` in all commands. This notoriously happens on Windows and macOS devices, as well as some Linux distributions.

## Initializing frontend

Please input the following commands in the project root directory:

- `yarn`
- `yarn dev`

## Testing backend

- `source env/bin/activate` (If Python source not already activated, see Initializing backend above)
- `python -m unittest discover -p "*_test.py"`

## Testing frontend

- `yarn test`

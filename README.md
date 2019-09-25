# Market-Admin

market-admin is a Market background management system with [fastapi](https://fastapi.tiangolo.com/).

## Contents

- [Installation](#installation)
- [Usage](#Usage)
- [License](#License)

## Installation
1. Get the project
```bash
go -get https://github.com/Huangkai1008/market-admin
```

2. Make sure you have installed [poetry](https://github.com/sdispater/poetry)
```bash
pip install poetry
```

## Usage

```bash
poetry install                  # Add the libs
poetry shell                    # Start the virtualenvs
uvicorn app.main:app --reload   # Start the uvicorn server
```

## License
[MIT](https://www.mit-license.org/)

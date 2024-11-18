### Setup

1. Install python version 3.13 with pyenv (skip if you already have one)
2. [Install poetry](https://python-poetry.org/docs/#installation) (skip if you already have one)
3. Install dependencies (skip if you already did)
   ```bash
   poetry shell
   poetry install
   ```
4. Create and fill `.env` file at root
5. Add your google cloud service account at root as
   ```bash
   sa-googlecloud.json
   ```
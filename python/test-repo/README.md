# MVP AI
This is a repository containing the work for the creation of AI MVP specifically all the AI code implementation

**CI/CD Status**:
<empty>

**Structure Folder**:
```bash
├── Dockerfile
├── README.md
├── main.py
├── pyproject.toml
├── pytest.ini
├── src
│   ├── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── middleware.py
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── aws.py
│   │   ├── const.py
│   │   ├── db.py
│   │   ├── log.py
│   │   ├── response.py
│   │   └── utils.py
│   └── modules
│       ├── information
│       │   ├── __init__.py
│       │   ├── schemas.py
│       │   └── views.py.py
│       ├── proposal
│       │   ├── __init__.py
│       │   ├── controllers.py
│       │   ├── knowledges
│       │   │   ├── __init__.py
│       │   │   ├── fore.py
│       │   │   ├── gokana.py
│       │   │   ├── saqu.py
│       │   │   └── yamazaki.py
│       │   ├── operators.py
│       │   ├── schemas.py
│       │   └── views.py.py
│       ├── survey
│       │   ├── __init__.py
│       │   ├── const.py
│       │   ├── controllers.py
│       │   ├── operators.py
│       │   ├── repositories.py
│       │   ├── schemas.py
│       │   └── views.py.py
│       └── webhook
└── tests
    ├── __init__.py
    ├── integration
    └── unit
```

To run the application in local environemnt, follow the steps below:
1. Make sure python version is similar to the given python version in `pyproject.toml` (you can use pyenv to achieve it, please refer to [this](https://medium.com/@adocquin/mastering-python-virtual-environments-with-pyenv-and-pyenv-virtualenv-c4e017c0b173) for tutorial how to install specific python version).
2. Install Poetry with version is similar to the provided version in Dockerfile.
3. Get in to Poetry shell.
    ```bash
    poetry shell
    ```
4. Install all dependencies (including dev) that are listed in `pyproject.toml`.
    ```bash
    poetry install
    ```
5. Run the application.
    ```bash
    python3 main.py
    ```

**Test Coverage**:
<empty>
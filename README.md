# garage inventory
inventory api with frontend to organize a virtual garage sale inventory


# poetry usage
```commandline
# install
poetry install

# testing + linting
poetry run pytest
poetry run flake8

# update python version
# the version must be installed and updated in the pyproject.toml
poetry env use 3.11

# add some dependencies
poetry add fastapi

# add some dependencies to dev
poetry add --group dev pytest pytest-cov

# build a wheel
poetry build -f wheel
```
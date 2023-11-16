# sale inventory
Inventory app to help organizing things on sale or to give away.
Components are: a fastapi backend with a sqlite database and a react frontend


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

# npm usage
```commandline
cd inventory-frontend

# run dev
npm start

# build
npm run build
```
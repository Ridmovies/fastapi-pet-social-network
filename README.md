### Run project
```bash
 uvicorn src.main:app --reload
```

### Openapi Documentation
http://127.0.0.1:8000/docs

# Develop
### Poetry Dependency Management System
### Creating a New Project

```bash
poetry new my-project
```
This command will create a new project structure with a `pyproject.toml` file where dependencies are stored.

### Initializing an Existing Project
```bash
poetry init
```

This command initializes the project by asking for necessary parameters and creating a `pyproject.toml` file.

### Adding a Package
```bash
poetry add requests
```
Adds the `requests` package to your project's list of dependencies.
To add a package under the `[tool.poetry.dev-dependencies]` section in the `pyproject.toml` file, use the following command:
```bash
poetry add <package-name> --group dev
```
### Updating All Packages
```bash
poetry update
```
Updates all packages to their latest compatible versions.

### Synchronizing Poetry with Virtual Environment
```bash
poetry install --sync
```
### Showing the Package Tree
```bash
poetry show --tree
```
### Removing a Package
```bash
poetry remove <package_name>
```


## Создание базы данных PostgreSQL через консоль 

### Шаг 1: Подключение к PostgreSQL
```bash
sudo -u postgres psql
```

### Шаг 2: Создание новой базы данных
```bash
CREATE DATABASE pet_social;
```

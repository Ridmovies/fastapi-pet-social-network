## Project status
- JWT auth
- Posts
- README
- Docker
- Nginx
- Front Interface


<!-- ROADMAP -->
## Roadmap

- [x] Poetry
- [x] Readme.md
- [x] .env Settings and Environment Variables 
- [x] async database
    - [x] Alembic
    - [ ] database for tests
    - [x] postgresql+asyncpg
- [x] example app "posts"
- [x] fix pytest mode
- [x] Auth app
    - [x] bearer access jwt token
    - [x] hashed password + salt
    - [x] refresh token
- [x] Admin Panel
- [x] Docker
    - [x] Docker compose

___

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Run project
```bash
 uvicorn src.main:app --reload
```

### Openapi Documentation
http://127.0.0.1:8000/docs


### Simple frontend interface
http://127.0.0.1:8000/tasks

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

### Шаг 3: Выйти с консоли PostgreSQL
```bash
    exit 
```


## Alembic

### Creating async an Environment
```bash
alembic init --template async alembic
```

### change env.py
?async_fallback=True для асинхронной базы
```
config = context.config
# if don't use --template async
# config.set_main_option("sqlalchemy.url", f"{settings.DATABASE_URL}?async_fallback=True")
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
target_metadata = Base.metadata
```
Импортируйте модели
```
from src.backend.dev.models import Song # noqa
from src.backend.products.models import Product # noqa
```

### Генерация первой миграции
```bash
alembic revision --autogenerate -m "initial migration"
```

### Примените созданную миграцию к базе данных:
```bash
alembic upgrade head
```

### Откатывает последнюю примененную миграцию.
```bash
alembic downgrade -1
```

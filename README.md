## Project status
- JWT auth
- Posts
- README
- Docker
- Nginx
- Front Interface


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

## Docker
## Commands for working with Docker and Docker Compose
These commands will help you manage containers and images in your project, providing a convenient development and testing process.

### Creating an image from a Dockerfile
```bash
docker build -t image_name .
```

### Run a container from an image
```bash
docker run -p 8000:8000 image_name
```

### Remove all containers
```bash
docker rm $(docker ps -aq)
```

### Remove all images
```bash
docker rmi $(docker images -q)
```

### Stop and remove all services and images

```bash
docker-compose down --rmi all
```

### To start a console inside a running Docker container, use the docker exec command
```bash
docker exec -it container_name bash
```

### Run the container in interactive mode to gain shell access inside the container:
```bash
docker run -it --rm -p 9000:8000 container_name sh
```


### Build a new image and run containers

```bash
docker-compose up --build
```
This command builds a new image based on the instructions in `docker-compose.yml`.
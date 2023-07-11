# test_task_for_Webtronics

Создать файл .env в корне проекта, внести следующие переменные:

```
POSTGRES_HOST=db

POSTGRES_PORT=5432

POSTGRES_DB=postgres

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

JWT_SECRET= {Любой JWT для работы fastapi-users}

CLEARBIT_KEY= {необходимо получить на clearbit. Токен указан на https://dashboard.clearbit.com/docs и начинается с "sk_" } 
```

________________________________________________________________

Развернуть в докере:
docker-compose up -d --build

swagger: localhost:8000/docs

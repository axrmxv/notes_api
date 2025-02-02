# notes_api


### Миграции

Инициализация миграций
```bash
alembic init migration
```

Создание миграций
```bash
alembic revision --autogenerate -m "init migration"
```

Применение миграций
```bash
alembic upgrade head
```

### Запустить проект
```bash
uvicorn app.main:app --host localhost --port 8050
```

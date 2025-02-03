# Notes API

API для управления заметками с использованием FastAPI, PostgreSQL и асинхронного SQLAlchemy.
Роли: **User** (работает только со своими заметками) и **Admin** (полный доступ).

---

## 🚀 Быстрый запуск

### Требования
- Docker и Docker Compose установленные на системе.

### Шаги
1. **Клонируйте репозиторий**
```bash
git clone https://github.com/axrmxv/notes_api.git
```
2. **Запустите проект через Docker Compose**
```bash
docker network create notes-network
docker-compose up -d
```
3. **Приложение будет доступно по адресу:**
- API: `http://localhost:8050`
- Документация Swagger: `http://localhost:8050/docs`

### Настройка окружения
**Переменные окружения**
- Создайте файл `.env` в корне проекта (пример):

```bash
DB_URL="postgresql+asyncpg://postgres:postgres@notes_db:5432/notes_db"
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_FILE="app.log"

NOTES_HOST=0.0.0.0
NOTES_PORT=8050
```

### Технологии
- **Backend**: FastAPI (Python)
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy (асинхронный режим)
- **Аутентификация**: OAuth2 с JWT
- **Логирование**: Встроенный модуль logging
- **Контейнеризация**: Docker + Docker Compose

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

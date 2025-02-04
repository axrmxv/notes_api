# Notes API

API для управления заметками с использованием FastAPI, PostgreSQL и асинхронного SQLAlchemy.
Роли: **User** (работает только со своими заметками) и **Admin** (полный доступ).

---

## Быстрый запуск

### Требования
- Docker и Docker Compose установленные на системе.

### Шаги
1. **Клонируйте репозиторий**
```bash
git clone https://github.com/username/notes_api.git
```
2. **Запустите базу данных**
```bash
cd notes_db
docker network create notes-network
docker-compose up -d
```
3. **Запустите проект через Docker Compose**
```bash
cd ..
docker-compose up -d
```
4. **Приложение будет доступно по адресу:**
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

Для генерации `secret_key` используйте команду:
```bash
openssl rand -hex 32
```

### Инициализация базы данных

При первом запуске приложения автоматически создаются необходимые таблицы в базе данных.

Также создается пользователь с правами администратора:

Логин: `admin`
Пароль: `adminpass`
Роль: `admin`

Пароль администратора хешируется для безопасного хранения в базе данных.

### Создание пользователей и тестовых данных

Для проверки работы API создайте тестовых пользователей и заметки вручную через запросы к API:
1. Создание пользователей:
```json
POST /register
{
  "username": "user1",
  "password": "user1pass",
  "role": "user"
}

POST /register
{
  "username": "user2",
  "password": "user2pass",
  "role": "user"
}
```
2. Создание заметок для пользователей:
После регистрации получите токены пользователей и создайте для них тестовые заметки:
```json
POST /api/v1/notes/
{
  "title": "string",
  "body": "string"
}
```

### Технологии
- **Backend**: FastAPI (Python)
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy (асинхронный режим)
- **Аутентификация**: OAuth2 с JWT
- **Логирование**: Встроенный модуль logging
- **Контейнеризация**: Docker + Docker Compose


### Запуск проекта без Docker
```bash
uvicorn app.main:app --host localhost --port 8050
```

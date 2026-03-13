├─ api/           # Backend API

backend/

app/

    main.py
    config.py

    api/
        router.py
        health.py
        items.py

    core/
        config.py
        security.py

    db/
        session.py
        base.py

    models/
        item.py

    schemas/
        item.py

    services/
        item_service.py

requirements.txt
Dockerfile


uvicorn app.main:app --reload
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
python-jose
passlib[bcrypt]
alembic
python-dotenv


миграция из app
python -m alembic revision --autogenerate -m "init"
python -m alembic upgrade head


запуск fastapi
uvicorn app.main:app --reload
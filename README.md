# UNN Student Voting Platform

### How to Run

Initial Working Directory Configuration

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Edit `.env`to reflect PostgreSql database url

```.env
DATABASE_URL=...
```

Rum Alembic Migration

```bash
alembic upgrade head
```

Start app
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

access App Swagger UI Docs at `localhost:5000/docs`

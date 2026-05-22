# UNN Student Voting Platform

### How to Run

Initial Working Directory Configuration

```bash
git clone <this repo url>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env_sample` to `.env` and edit PostgreSql database url and JWT_SECRET_KEY

```.env
DATABASE_URL=...

JWT_SECRET_KEY=...
```

Rum Alembic Migration

```bash
alembic upgrade head
```

Start app
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

Access App Swagger UI Docs at `localhost:5000/docs`

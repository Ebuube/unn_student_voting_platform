from datetime import datetime, timedelta, UTC

import jwt

from app.config import settings


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_expire_minutes,
    )

    payload.update({
        "exp": expire,
    })

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return token

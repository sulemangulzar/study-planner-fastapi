from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from src.config import settings


def create_access_token(
    data: dict,
    expiry: timedelta = timedelta(hours=1),
):
    token = jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token

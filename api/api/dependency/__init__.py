import logging

import jwt
from fastapi import Header, status, HTTPException
from httpx import AsyncClient
from sqlmodel import select

from .db import get_db_session, safe_db_read
from ..model.orm import User

log = logging.getLogger(__name__)

environment_id = "b1c47bc4-7e96-451e-a937-f85fa7226bfb"
dynamic_api_key = "dyn_puLvWKrjUbDF1ACufYX2gYyJ7KPkFCJZ9W2Ew8E1ym1zBzXfNT3aur5d"


def verify_jwt(token, secret_key):
    try:
        # Decode the JWT using the secret key
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return None


async def get_user(x_fortuna_jwt: str = Header(None)) -> User:
    db_session = next(get_db_session())
    # "undefined" is the string that is sent when the header is not present because _javaaascript_
    if x_fortuna_jwt is None or x_fortuna_jwt == "undefined":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing JWT")
    else:
        async with AsyncClient() as client:
            r = await client.get(f"https://app.dynamicauth.com/api/v0/environments/{environment_id}/keys",
                                 headers={"Authorization": f"Bearer {dynamic_api_key}"})
            if r.status_code == status.HTTP_200_OK:
                env_keys = r.json()
                log.info(env_keys)
                # TODO fix the jwt verification
                # decoded_jwt = verify_jwt(x_fortuna_jwt, env_keys["key"]["publicKey"])
                # log.info(decoded_jwt)
                try:
                    db_user = safe_db_read(select(User).where(User.uid == "TODO"), db_session)
                    return db_user
                except HTTPException as not_found:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            else:
                log.info(r.status_code)
                log.info(r.text)
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid JWT")

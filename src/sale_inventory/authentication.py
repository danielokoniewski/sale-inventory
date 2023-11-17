from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel
from starlette.responses import Response

# Secret key to sign JWT tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


class User(BaseModel):
    username: str
    full_name: str
    email: str


# In-memory user database (replace with a real database in production)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedpassword",
    }
}


def create_jwt_token(username: str) -> str:
    """
    return a jwt token with only the username
    """
    token_data = {"sub": username}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def set_jwt_cookie(token: str) -> Response:
    """
    sets the jwt as cookie with name "token"
    """
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="token", value=token)
    return response


def get_current_user(request: Request) -> dict:
    """
    depends on having a cookie/ later: or basic auth/Bearer Token
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #  first get the Token
    token = request.cookies.get("token")
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        if username not in fake_users_db:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return fake_users_db.get(username)


auth_router = APIRouter()


@auth_router.get("/user", response_model=User)
async def get_user(current_user: Annotated[dict, Depends(get_current_user)]) -> User:
    """
    Shows the information about the current user
    needs a /token to work
    """
    return User(**current_user)


@auth_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Response:
    """
    Check the credentials against a not at all fake user database
    """
    user = fake_users_db.get(form_data.username)
    if user is None or form_data.password != "fakepassword":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    token = create_jwt_token(form_data.username)

    # Set JWT token in a cookie
    return set_jwt_cookie(token)


@auth_router.post("/logout")
async def logout(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Logout route to invalidate the token (client-side implementation)
    """
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie(key="token")
    return response

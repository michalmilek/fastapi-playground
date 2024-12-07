from app.utils.password import hash_password
from app.utils.token import create_tokens, refresh_access_token, verify_token
from app.schemas import UserRegisterSchema, UserLoginSchema
from app.models import user as user_model
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.database import get_db

router = APIRouter()

security = HTTPBearer()

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User successfully registered"
        }
    }
)
async def register(user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    hashed_password = hash_password(user_data.password)
    
    new_user = user_model.User(
        email=user_data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return Response(status_code=status.HTTP_201_CREATED)

@router.post("/login")
def login(user_data: UserLoginSchema):
    # Verify user credentials here
    user_data = {"sub": user_data.email}  # Add any user data you want in the token
    return create_tokens(user_data)

# Example token refresh
@router.post("/refresh")
def refresh_token(refresh_token: str):
    new_access_token = refresh_access_token(refresh_token)
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    return {"access_token": new_access_token, "token_type": "bearer"}

# Example protected endpoint
@router.get("/protected")
def protected_route(auth: HTTPAuthorizationCredentials = Security(security)):
    payload = verify_token(auth.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"message": "Access granted", "user": payload.get("sub")}
    
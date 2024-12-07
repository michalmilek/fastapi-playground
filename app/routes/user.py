from app.schemas import UserBaseSchema
from app.models import user as user_model
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from app.config.database import get_db

router = APIRouter()
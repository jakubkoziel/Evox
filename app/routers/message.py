from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import schemas, database
from app.services import message
from app.security import verify_api_key

router = APIRouter(
    prefix='/messages',
    tags=["messages"]
)

get_db = database.get_db


@router.get('/{id}', response_model=schemas.MessageView)
async def get_message(id: int, db: Session = Depends(get_db)):
    return message.get(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_message(request: schemas.Message, db: Session = Depends(get_db), authentication: bool = Depends(verify_api_key)):
    return message.create(request, db)


@router.put('/{id}', status_code=status.HTTP_200_OK)
async def update_message(id: int, request: schemas.Message, db: Session = Depends(get_db), authentication: bool = Depends(verify_api_key)):
    return message.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_message(id: int, db: Session = Depends(get_db), authentication: bool = Depends(verify_api_key)):
    return message.delete(id, db)

from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status


def get(id: int, db: Session):
    message = db.query(models.Message).filter(models.Message.id == id)

    if not message.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with id {id} not found.")

    # increase number of views witch each get
    message.update({"counter": message.first().counter + 1})
    db.commit()
    db.refresh(message.first())

    return message.first()


def create(request: schemas.Message, db: Session):
    new_message = models.Message(content=request.content)

    length_validator(new_message)

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def delete(id: int, db: Session):
    message = db.query(models.Message).filter(models.Message.id == id)
    if not message.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with id {id} not found.")

    message.delete(synchronize_session=False)
    db.commit()
    return message


def update(id: int, request: schemas.Message, db: Session):
    message = db.query(models.Message).filter(models.Message.id == id)

    if not message.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with id {id} not found.")

    message.update({"content": request.content, "counter": 0})

    length_validator(message.first())

    db.commit()
    return message.first()


def length_validator(message: schemas.MessageView):
    if message.content is None or len(message.content) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty")

    if len(message.content) > 160:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Message content cannot exceed 160 characters.")

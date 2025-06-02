from sqlalchemy.orm import Session
from models.mtm_orm_model import MTMRecordORM as MTMRecord

def get_record_by_id(db: Session, transaction_id: str):
    return db.query(MTMRecord).filter(MTMRecord.TRANSACTION_ID == transaction_id).first()

def get_all_records(db: Session):
    return db.query(MTMRecord).all()

def create_record(db: Session, record: MTMRecord):
    # Convert Pydantic model to ORM model
    orm_record = MTMRecord(**record.dict())

    db.add(orm_record)
    db.commit()
    db.refresh(orm_record)
    return orm_record

def delete_record_by_id(db: Session, transaction_id: str):
    record = db.query(MTMRecord).filter(MTMRecord.TRANSACTION_ID == transaction_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record

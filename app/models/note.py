from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.connection import Base

class Note(Base):

    __tablename__ = "notes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(String)

    content = Column(String)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id")
    )

    owner = relationship("Subject")
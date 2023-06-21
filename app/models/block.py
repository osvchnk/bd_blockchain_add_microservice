from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Block(Base):
    __tablename__ = "block"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    prev_hash = Column(String, nullable=False)
    hash = Column(String, nullable=False, unique=True)
    admin_sign = Column(String, nullable=False)

    transactions = relationship("TransactionInBlock", back_populates="block")


class TransactionInBlock(Base):
    __tablename__ = "transaction_in_block"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, nullable=False)

    block_id = Column(Integer, ForeignKey("block.id"))
    block = relationship("Block", back_populates="transactions")

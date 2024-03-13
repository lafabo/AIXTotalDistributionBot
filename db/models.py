# -*- coding: utf-8 -*-
"""
SQLAlchemy TotalDistributionEvent Model
"""
from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base


Base = declarative_base()

@dataclass
class TotalDistributionEvent(Base):
    __tablename__ = "total_distribution_events"
    id: int = Column(Integer, primary_key=True)
    block: BigInteger = Column(BigInteger)
    tx_hash: str = Column(String)
    timestamp: DateTime = Column(DateTime)  # storing in UTC time
    distributor_wallet: str = Column(String)
    input_aix_amount: DECIMAL = Column(DECIMAL(precision=38, scale=0))
    distributed_aix_amount: DECIMAL = Column(DECIMAL(precision=38, scale=0))
    swapped_eth_amount: DECIMAL = Column(DECIMAL(precision=38, scale=0))
    distributed_eth_amount: DECIMAL = Column(DECIMAL(precision=38, scale=0))

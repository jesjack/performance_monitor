import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.performance_monitor_jesjack.models.base import Base


class ExecutionSession(Base):
    __tablename__ = 'execution_session'

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    execution_metrics = relationship('ExecutionMetric',
                                     back_populates='execution_session',
                                     cascade='all, delete-orphan')

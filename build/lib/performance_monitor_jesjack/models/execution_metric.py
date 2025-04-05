from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.orm import relationship

from src.performance_monitor_jesjack.models.base import Base
from src.performance_monitor_jesjack.models.execution_session import ExecutionSession


class ExecutionMetric(Base):
    __tablename__ = 'execution_metrics'

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    function_name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    execution_session = relationship('ExecutionSession',
                                     backref='execution_metrics',
                                     cascade='all, delete-orphan')

    @classmethod
    def add_metric(cls, session, function_name, start_time, end_time, execution_session):
        """
        Adds a metric to the database.
        :param session: The SQLAlchemy session.
        :param function_name: The name of the function.
        :param start_time: The start time of the function execution.
        :param end_time: The end time of the function execution.
        :param execution_session: The execution session object.
        """
        metric = cls(
            function_name=function_name,
            start_time=start_time,
            end_time=end_time,
            execution_session=execution_session
        )
        session.add(metric)
        session.commit()
        return metric
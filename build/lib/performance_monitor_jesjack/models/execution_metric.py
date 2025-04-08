from typing import Optional

from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, desc, func
from sqlalchemy.orm import relationship, Session

from src.performance_monitor_jesjack.models.base import Base
from src.performance_monitor_jesjack.models.execution_session import ExecutionSession


class ExecutionMetric(Base):
    __tablename__ = 'execution_metrics'

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    function_name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    execution_session_id = Column(String, ForeignKey('execution_session.session_id'))
    execution_session = relationship('ExecutionSession',
                                     back_populates='execution_metrics')

    def total_time(self) -> float:
        """
        Returns the total execution time in milliseconds.
        :return: Total execution time in milliseconds.
        """
        return self.end_time.timestamp() - self.start_time.timestamp()


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
        assert isinstance(session, Session)
        metric = cls(
            function_name=function_name,
            start_time=start_time,
            end_time=end_time,
            execution_session=execution_session
        )
        session.add(metric)
        session.commit()
        return metric

    @classmethod
    def get_metrics(cls, session, session_id: Optional[str] = None,
                    function_name: Optional[str] = None,
                    max_sessions: Optional[int] = None):
        """
        Retrieves metrics from the database.
        :param max_sessions: The maximum number of sessions to retrieve.
        :param session: The SQLAlchemy session.
        :param session_id: The ID of the execution session.
        :param function_name: The name of the function.
        :return: A list of metrics.
        """
        assert isinstance(session, Session)
        query = session.query(cls)
        if session_id:
            query = query.filter(cls.execution_session_id == session_id)
        if function_name:
            query = query.filter(cls.function_name == function_name)
        if max_sessions:
            subquery = (session.query(cls.execution_session_id, func.min(cls.start_time).label('min_start_time'))
                        .group_by(cls.execution_session_id)
                        .order_by(desc('min_start_time'))
                        .limit(max_sessions)
                        .subquery())
            query = query.join(subquery, cls.execution_session_id == subquery.c.execution_session_id)
        return query.all()
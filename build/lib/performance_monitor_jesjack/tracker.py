from asyncio import iscoroutinefunction
from datetime import datetime
from functools import wraps
from time import time

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.performance_monitor_jesjack.models.base import Base
from src.performance_monitor_jesjack.models.execution_metric import ExecutionMetric
from src.performance_monitor_jesjack.models.execution_session import ExecutionSession


class ExecutionTracker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ExecutionTracker, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.db_uri = "execution_data.db"
        self.engine = create_engine(f'sqlite:///{self.db_uri}')
        Base.metadata.create_all(self.engine)
        self.execution_session = ExecutionSession()
        pass

    def _mid_wrapper(self, result, start_time, func):
        """
        This function is called after the function execution to store the metrics.
        :param result:
        :param start_time:
        :return:
        """
        end_time = datetime.now()

        with Session(self.engine) as session:
            ExecutionMetric.add_metric(session,
                                       function_name=func.__name__,
                                       start_time=start_time,
                                       end_time=end_time,
                                       execution_session=self.execution_session)

        return result

    def timing_decorator(self, func):
        """
        Gets the execution time of a function and stores the results.
        :param func:
        :return:
        """
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            return self._mid_wrapper(result, start_time, func)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = await func(*args, **kwargs)
            return self._mid_wrapper(result, start_time, func)

        if iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
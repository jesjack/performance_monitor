from src.performance_monitor_jesjack.tracker import ExecutionTracker

_tracker = ExecutionTracker()

def timeit(func):
    """
    Decorator to measure the execution time of a function.
    :param func: The function to be decorated.
    :return: The decorated function.
    """
    return _tracker.timing_decorator(func)
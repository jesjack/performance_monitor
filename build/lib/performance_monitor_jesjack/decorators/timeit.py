from src.performance_monitor_jesjack.graphing import ExecutionGraphing

class TimeitDecorator:
    def __init__(self, tracker):
        self.tracker = tracker

    def __call__(self, func):

        return self.tracker.timing_decorator(func)

    def show(self, func):
        """
        Decorator to measure the execution time of a function and show the graph at exit.
        :param func: The function to be decorated.
        :return: The decorated function.
        """
        wrapped_func = self.tracker.timing_decorator(func)
        ExecutionGraphing._plot_on_exit(function_name=func.__name__)
        return wrapped_func
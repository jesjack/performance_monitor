from src.performance_monitor_jesjack.decorators.timeit import TimeitDecorator
from src.performance_monitor_jesjack.tracker import ExecutionTracker
from src.performance_monitor_jesjack.graphing import ExecutionGraphing

_tracker = ExecutionTracker()


timeit = TimeitDecorator(_tracker)
"""
Module for performance monitoring and execution time tracking.
This module provides decorators to measure the execution time of functions
and visualize the execution graph.
"""

show_graph = ExecutionGraphing(_tracker)
"""
Module for visualizing execution graphs.
This module provides functionality to plot the execution graph
of functions over different sessions.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import atexit
import signal

from src.performance_monitor_jesjack.models.execution_metric import ExecutionMetric
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

class ExecutionGraphing:

    def __init__(self, _tracker):
        self._tracker = _tracker

    def __call__(self):
        """
        This method is called to plot the graph.
        It retrieves the execution metrics and plots them.
        """
        self._plot_graph()

    def on_exit(self, function_name=None):
        """
        This method is called to plot the graph on exit.
        It registers the signal handlers for SIGINT and SIGTERM.
        """
        self._plot_on_exit(function_name=function_name)

    @classmethod
    def _plot_graph(cls, function_name=None):
        # Create a new SQLAlchemy session
        engine = create_engine('sqlite:///execution_data.db')
        with Session(engine) as session:
            # Retrieve the metrics for the specified function
            metrics = ExecutionMetric.get_metrics(session,
                                                  function_name=function_name,
                                                  max_sessions=5)

            if not metrics:
                print(f"No metrics found for functions")
                return

            # Extract the start and end times
            # start_times = [metric.start_time for metric in metrics]
            # end_times = [metric.end_time for metric in metrics]
            function_names = [metric.function_name for metric in metrics]
            session_ids = [metric.execution_session.session_id for metric in metrics]
            total_times = [metric.total_time() for metric in metrics]

        # Create a DataFrame for the plot
        df = pd.DataFrame({
            'Session': session_ids,
            'Total Time': total_times,
            'Function Name': function_names
        })

        x = df['Total Time']
        x_centered = (x - x.mean()) / x.std()  # centrado y normalizado

        # Ajuste más agresivo con tanh
        scale_factor = 3  # prueba con valores entre 1 y 3
        df['Total Time (scaled)'] = np.tanh(scale_factor * x_centered)

        # Gráfico
        fig = px.violin(df, x='Session', y='Total Time (scaled)', color='Function Name', box=True, points="all",
                        hover_data={'Total Time': True})
        fig.update_yaxes(title='Scaled Total Time (tanh-adjusted)')
        fig.show()

    @classmethod
    def _plot_on_exit(cls, function_name=None):
        """
        Plot the execution time of functions over different sessions when the program exits.
        """
        atexit.register(cls._plot_graph, function_name=function_name)

        def handle_signal(signum, frame):
            cls._plot_graph(function_name=function_name)
            raise SystemExit(f'Program terminated with signal {signum}')

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

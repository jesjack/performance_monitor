import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.performance_monitor_jesjack.models.execution_metric import ExecutionMetric
from src.performance_monitor_jesjack.models.execution_session import ExecutionSession
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

class ExecutionGraphing:

    @classmethod
    def plot_graph(cls, function_name):
        """
        Plots a 3D bar graph of the execution metrics for a given function.
        :param function_name: The name of the function to plot.
        """

        # Create a new SQLAlchemy session
        engine = create_engine('sqlite:///execution_data.db')
        with Session(engine) as session:
            # Retrieve the metrics for the specified function
            metrics = ExecutionMetric.get_metrics(session, function_name=function_name)

            if not metrics:
                print(f"No metrics found for function: {function_name}")
                return

            # Extract the start and end times
            start_times = [metric.start_time for metric in metrics]
            end_times = [metric.end_time for metric in metrics]
            function_names = [metric.function_name for metric in metrics]
            session_ids = [metric.execution_session.session_id for metric in metrics]
            total_times = [metric.total_time() for metric in metrics]

        # Create a DataFrame
        df = pd.DataFrame({
            'Session ID': session_ids,
            'Function Name': function_names,
            'Total Time (ms)': total_times
        })

        # Create 3D bar plot
        fig = go.Figure(data=[go.Bar3d(
            x=df['Session ID'],
            y=df['Total Time (ms)'],
            z=df['Function Name'],
            text=df['Function Name'],
            hoverinfo='text',
            opacity=0.8
        )])

        fig.update_layout(
            title=f'3D Bar Plot for {function_name}',
            scene=dict(
                xaxis_title='Session ID',
                yaxis_title='Total Time (ms)',
                zaxis_title='Function Name'
            )
        )

        fig.show()
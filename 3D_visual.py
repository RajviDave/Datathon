import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from IPython.display import HTML
import plotly.io as pio

# Set default template for better looking plots
pio.templates.default = "plotly_dark"

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def create_animated_traffic_flow(df):
    # Create an animated scatter plot showing vehicle movement over time
    fig = px.scatter(df, 
                    x='VEHS(ALL)_1',
                    y='SPEEDAVGARITH(ALL)_1',
                    animation_frame=df.index,
                    size='OCCUPRATE(ALL)_1',
                    color='QUEUEDELAY(ALL)_1',
                    range_color=[0, df['QUEUEDELAY(ALL)_1'].max()],
                    size_max=50,
                    title='Traffic Flow Animation (Segment 1)')
    
    fig.update_layout(
        xaxis_title="Number of Vehicles",
        yaxis_title="Average Speed",
        showlegend=True,
        template="plotly_dark"
    )
    
    return fig

def create_realtime_traffic_dashboard(df):
    # Create a dashboard with multiple interactive plots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Speed vs Occupancy', 'Vehicle Count vs Delay',
                       'Speed Distribution', 'Traffic Flow Timeline'),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'violin'}, {'type': 'scatter'}]]
    )
    
    # Speed vs Occupancy
    for i in range(1, 7):
        fig.add_trace(
            go.Scatter(
                x=df[f'SPEEDAVGARITH(ALL)_{i}'],
                y=df[f'OCCUPRATE(ALL)_{i}'],
                mode='markers',
                name=f'Segment {i}',
                marker=dict(size=8),
            ),
            row=1, col=1
        )
    
    # Vehicle Count vs Delay
    for i in range(1, 7):
        fig.add_trace(
            go.Scatter(
                x=df[f'VEHS(ALL)_{i}'],
                y=df[f'QUEUEDELAY(ALL)_{i}'],
                mode='markers+lines',
                name=f'Segment {i}',
            ),
            row=1, col=2
        )
    
    # Speed Distribution
    for i in range(1, 7):
        fig.add_trace(
            go.Violin(
                y=df[f'SPEEDAVGARITH(ALL)_{i}'],
                name=f'Segment {i}',
                box_visible=True,
                meanline_visible=True,
            ),
            row=2, col=1
        )
    
    # Traffic Flow Timeline
    for i in range(1, 7):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[f'VEHS(ALL)_{i}'],
                mode='lines',
                name=f'Segment {i}',
                fill='tonexty',
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        height=800,
        title_text="Interactive Traffic Analysis Dashboard",
        showlegend=True,
        template="plotly_dark"
    )
    
    return fig

def create_3d_traffic_flow(df):
    # Create an animated 3D visualization
    fig = go.Figure()
    
    for i in range(1, 7):
        fig.add_trace(go.Scatter3d(
            x=df[f'VEHS(ALL)_{i}'],
            y=df[f'SPEEDAVGARITH(ALL)_{i}'],
            z=df[f'OCCUPRATE(ALL)_{i}'],
            mode='markers',
            marker=dict(
                size=df[f'QUEUEDELAY(ALL)_{i}']/10,
                color=df[f'QUEUEDELAY(ALL)_{i}'],
                colorscale='Viridis',
                opacity=0.8
            ),
            name=f'Segment {i}'
        ))
    
    fig.update_layout(
        title='3D Traffic Flow Analysis',
        scene=dict(
            xaxis_title='Vehicle Count',
            yaxis_title='Average Speed',
            zaxis_title='Occupancy Rate'
        ),
        height=800
    )
    
    return fig

def main():
    # Load data
    file_path = r"C:\Users\Priyesh Vagadia\Downloads\datathon.csv"
    df = load_data(file_path)
    df = df.head(500)
    
    # Create visualizations
    traffic_flow_animation = create_animated_traffic_flow(df)
    traffic_dashboard = create_realtime_traffic_dashboard(df)
    traffic_3d = create_3d_traffic_flow(df)
    
    # Save as HTML files for interactivity
    traffic_flow_animation.write_html("traffic_flow_animation.html")
    traffic_dashboard.write_html("traffic_dashboard.html")
    traffic_3d.write_html("traffic_3d.html")
    
    # Show plots (if running in notebook)
    traffic_flow_animation.show()
    traffic_dashboard.show()
    traffic_3d.show()

if __name__ == "__main__":
    main()
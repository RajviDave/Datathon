import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def load_data(file_path):
    return pd.read_csv(file_path)

def create_animated_occupancy_visualization(df):
    # Create figure
    fig = go.Figure()
    
    # Create animation frames for each time interval
    frames = []
    for time_idx in df.index:
        frame_data = []
        
        for segment in range(1, 7):
            # Calculate positions for vehicle icons
            num_vehicles = df.iloc[time_idx][f'VEHS(ALL)_{segment}']
            occupancy = df.iloc[time_idx][f'OCCUPRATE(ALL)_{segment}']
            
            # Create road segment visualization
            frame_data.append(
                go.Scatter(
                    x=[segment]*int(min(num_vehicles/10, 20)),  # Scale down number of dots for visibility
                    y=np.random.uniform(0, occupancy, int(min(num_vehicles/10, 20))),
                    mode='markers',
                    marker=dict(
                        symbol='square',
                        size=20,
                        color=occupancy,
                        colorscale='RdYlBu_r',
                        showscale=True,
                        colorbar=dict(title='Occupancy Rate')
                    ),
                    name=f'Segment {segment}'
                )
            )
        
        frames.append(go.Frame(data=frame_data, name=str(time_idx)))
    
    # Add initial data
    for trace in frames[0].data:
        fig.add_trace(trace)
    
    # Update layout with animation settings
    fig.update_layout(
        title='Road Occupancy Animation',
        xaxis=dict(title='Road Segments', range=[0, 7]),
        yaxis=dict(title='Road Width', range=[0, df[[col for col in df.columns if 'OCCUP' in col]].max().max()]),
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
            }]
        }],
        sliders=[{
            'currentvalue': {'prefix': 'Time: '},
            'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                       'label': f'Time {k}',
                       'method': 'animate'} for k, f in enumerate(frames)]
        }]
    )
    
    fig.frames = frames
    return fig

def create_speed_flow_animation(df):
    fig = go.Figure()
    
    frames = []
    for time_idx in df.index:
        frame_data = []
        
        for segment in range(1, 7):
            speed = df.iloc[time_idx][f'SPEEDAVGARITH(ALL)_{segment}']
            vehicles = df.iloc[time_idx][f'VEHS(ALL)_{segment}']
            delay = df.iloc[time_idx][f'QUEUEDELAY(ALL)_{segment}']
            
            # Create flowing traffic visualization
            frame_data.append(
                go.Scatter(
                    x=np.linspace(0, speed, int(vehicles/10)),
                    y=[segment]*int(vehicles/10),
                    mode='markers',
                    marker=dict(
                        symbol='triangle-right',
                        size=15,
                        color=delay,
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title='Queue Delay')
                    ),
                    name=f'Segment {segment}'
                )
            )
        
        frames.append(go.Frame(data=frame_data, name=str(time_idx)))
    
    # Add initial data
    for trace in frames[0].data:
        fig.add_trace(trace)
    
    fig.update_layout(
        title='Traffic Speed and Flow Animation',
        xaxis=dict(title='Speed', range=[0, df[[col for col in df.columns if 'SPEED' in col]].max().max()]),
        yaxis=dict(title='Road Segments', range=[0, 7]),
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
            }]
        }]
    )
    
    fig.frames = frames
    return fig

def create_combined_metrics_animation(df):
    fig = make_subplots(rows=2, cols=1, 
                       specs=[[{'type': 'scatter'}],
                             [{'type': 'scatter'}]],
                       subplot_titles=('Traffic Density vs Speed', 'Queue Delay Impact'))
    
    frames = []
    for time_idx in df.index:
        frame_data = []
        
        for segment in range(1, 7):
            speed = df.iloc[time_idx][f'SPEEDAVGARITH(ALL)_{segment}']
            vehicles = df.iloc[time_idx][f'VEHS(ALL)_{segment}']
            occupancy = df.iloc[time_idx][f'OCCUPRATE(ALL)_{segment}']
            delay = df.iloc[time_idx][f'QUEUEDELAY(ALL)_{segment}']
            
            # Top plot: Speed vs Density
            frame_data.append(
                go.Scatter(
                    x=[vehicles],
                    y=[speed],
                    mode='markers',
                    marker=dict(
                        size=occupancy*10,
                        color=occupancy,
                        colorscale='RdYlBu_r',
                        showscale=True
                    ),
                    name=f'Segment {segment}',
                    xaxis='x1',
                    yaxis='y1'
                )
            )
            
            # Bottom plot: Delay Impact
            frame_data.append(
                go.Scatter(
                    x=[vehicles],
                    y=[delay],
                    mode='markers',
                    marker=dict(
                        size=speed/5,
                        color=delay,
                        colorscale='Viridis',
                        showscale=True
                    ),
                    name=f'Segment {segment}',
                    xaxis='x2',
                    yaxis='y2'
                )
            )
        
        frames.append(go.Frame(data=frame_data, name=str(time_idx)))
    
    # Add initial data
    for trace in frames[0].data:
        fig.add_trace(trace)
    
    fig.update_layout(
        height=800,
        title_text="Traffic Metrics Relationships",
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
            }]
        }]
    )
    
    fig.frames = frames
    return fig

def main():
    # Load data
    file_path = r"C:\Users\Priyesh Vagadia\Downloads\datathon.csv"
    df = load_data(file_path)
    df = df.head(500)
    
    # Create visualizations
    occupancy_fig = create_animated_occupancy_visualization(df)
    speed_flow_fig = create_speed_flow_animation(df)
    metrics_fig = create_combined_metrics_animation(df)
    
    # Save interactive HTML files
    occupancy_fig.write_html("occupancy_animation.html")
    speed_flow_fig.write_html("speed_flow_animation.html")
    metrics_fig.write_html("metrics_animation.html")
    
    # Display figures (if in notebook)
    occupancy_fig.show()
    speed_flow_fig.show()
    metrics_fig.show()

if __name__ == "__main__":
    main()
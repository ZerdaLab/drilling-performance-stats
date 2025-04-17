import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def basic_box_plot(dh_df, target_column='OBR', color='#1f77b4'):
    """
    Creates a basic boxplot of a single column with statistics table.
    """
    # Calculate statistics
    clean_data = dh_df[target_column].dropna()
    stats = {
        'Statistic': ['Count', 'Mean', 'Median', 'Min', 'Max', 'P10', 'P90', 'Std Dev'],
        'Value': [
            len(clean_data),
            np.mean(clean_data),
            np.median(clean_data),
            np.min(clean_data),
            np.max(clean_data),
            np.percentile(clean_data, 10),
            np.percentile(clean_data, 90),
            np.std(clean_data)
        ]
    }
    
    # Format values
    stats['Value'] = [f"{x:.2f}" if isinstance(x, (float, np.floating)) else str(x) 
                     for x in stats['Value']]
    
    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=1,
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "box"}], [{"type": "table"}]]
    )
    
    # Add box plot trace (top subplot)
    fig.add_trace(
        go.Box(
            y=clean_data,
            name=target_column,
            marker_color=color,
            boxmean='sd'
        ),
        row=1, col=1
    )
    
    # Add horizontal lines for key statistics (top subplot)
    mean = float(stats['Value'][1])
    median = float(stats['Value'][2])
    
    fig.add_hline(
        y=mean,
        line_dash="dash",
        line_color="blue",
        annotation_text=f"Mean: {mean:.2f}",
        annotation_position="bottom right",
        row=1, col=1
    )
    
    fig.add_hline(
        y=median,
        line_dash="dot",
        line_color="red",
        annotation_text=f"Median: {median:.2f}",
        annotation_position="bottom right",
        row=1, col=1
    )
    
    # Add statistics table (bottom subplot)
    fig.add_trace(
        go.Table(
            header=dict(
                values=list(stats.keys()),
                font=dict(size=12),
                align="left"
            ),
            cells=dict(
                values=[stats[key] for key in stats.keys()],
                align="left",
                font=dict(size=11)
            )
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"Distribution of {target_column}",
        yaxis_title=target_column,
        showlegend=False,
        height=700,
        margin=dict(t=80, b=20)
    )
    
    fig.show()



def boxplot_split_by_runs(dh_df, runs_df, target_column):
    """
    Creates box plots split by drilling runs with integrated stats table.
    """
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "box"}], [{"type": "table"}]]
    )
    
    # Color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Statistics storage
    stats_data = {
        'Bit Model': [],
        'Count': [],
        'Mean': [],
        'Median': [],
        'Min': [],
        'Max': [],
        'Std Dev': []
    }
    
    # Process each run
    for run_idx, run in runs_df.iterrows():
        bit_model = run['bit model']
        depth_in = run['depth in']
        depth_out = run['depth out']
        color = colors[run_idx % len(colors)]
        
        # Filter run data
        run_data = dh_df[
            (dh_df['DEPT'] >= depth_in) & 
            (dh_df['DEPT'] <= depth_out)
        ][target_column].dropna()

        if run_data.empty:
            continue
        
        # Calculate stats
        stats = {
            'count': len(run_data),
            'mean': np.mean(run_data),
            'median': np.median(run_data),
            'min': np.min(run_data),
            'max': np.max(run_data),
            'std': np.std(run_data)
        }
        
        # Store stats
        stats_data['Bit Model'].append(bit_model)
        stats_data['Count'].append(stats['count'])
        stats_data['Mean'].append(f"{stats['mean']:.2f}")
        stats_data['Median'].append(f"{stats['median']:.2f}")
        stats_data['Min'].append(f"{stats['min']:.2f}")
        stats_data['Max'].append(f"{stats['max']:.2f}")
        stats_data['Std Dev'].append(f"{stats['std']:.2f}")
        
        # Add boxplot (top subplot)
        fig.add_trace(
            go.Box(
                y=run_data,
                name=bit_model,
                marker_color=color,
                boxmean=True,
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Add table (bottom subplot)
    fig.add_trace(
        go.Table(
            header=dict(
                values=list(stats_data.keys()),
                font=dict(size=12),
                align="left"
            ),
            cells=dict(
                values=[stats_data[key] for key in stats_data.keys()],
                align="left",
                font=dict(size=11)
            )
        ),
        row=2, col=1
    )
    
    # Update layout for proper display
    fig.update_layout(
        title=f"{target_column} Distribution by Bit Run",
        yaxis_title=target_column,
        xaxis_title="Bit Model",
        xaxis_type='category', 
        height=800,
        margin=dict(t=80, b=80),
        showlegend=False
    )
    
    fig.show()



def boxplot_by_runs_and_formations(dh_df, runs_df, forms_df, target_column):
    """
    Creates box plots split by drilling runs AND formations with integrated stats table.
    """
    # Sort formations by depth
    forms_df = forms_df.sort_values('Depth')
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "box"}], [{"type": "table"}]]
    )
    
    # Color palette for runs
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Statistics storage
    stats_data = {
        'Bit Model': [],
        'Formation': [],
        'From (m)': [],
        'To (m)': [],
        'Count': [],
        'Mean': [],
        'Median': [],
        # 'Std Dev': [],
        'P90': []
    }
    
    # Process each run
    for run_idx, run in runs_df.iterrows():
        bit_model = run['bit model']
        run_start = run['depth in']
        run_end = run['depth out']
        color = colors[run_idx % len(colors)]
        
        # Filter data for this run's depth range
        run_data = dh_df[
            (dh_df['DEPT'] >= run_start) & 
            (dh_df['DEPT'] <= run_end)
        ].copy()
        
        if run_data.empty:
            continue
        
        # Process formations within this run
        for form_idx, formation in forms_df.iterrows():
            form_name = formation['Formation']
            form_start = formation['Depth']
            
            # Skip formations that start above the run
            if form_start >= run_end:
                break
            
            # Determine the segment's start and end
            segment_start = max(form_start, run_start)
            if form_idx + 1 < len(forms_df):
                next_form_start = forms_df.iloc[form_idx + 1]['Depth']
                segment_end = min(next_form_start, run_end)
            else:
                segment_end = run_end  # Last formation extends to the run's end
            
            # Skip if the segment is outside the run's range
            if segment_start >= segment_end:
                continue
            
            # Filter data for this formation segment
            segment_data = run_data[
                (run_data['DEPT'] >= segment_start) & 
                (run_data['DEPT'] < segment_end)
            ][target_column].dropna()
            
            if segment_data.empty:
                continue
            
            # Calculate statistics
            stats = {
                'count': len(segment_data),
                'mean': np.mean(segment_data),
                'median': np.median(segment_data),
                # 'std': np.std(segment_data),
                'p90': np.percentile(segment_data, 90),
            }
            
            # Store stats
            stats_data['Bit Model'].append(bit_model)
            stats_data['Formation'].append(form_name)
            stats_data['From (m)'].append(f"{segment_start:.1f}")
            stats_data['To (m)'].append(f"{segment_end:.1f}")
            stats_data['Count'].append(stats['count'])
            stats_data['Mean'].append(f"{stats['mean']:.2f}")
            stats_data['Median'].append(f"{stats['median']:.2f}")
            # stats_data['Std Dev'].append(f"{stats['std']:.2f}")
            stats_data['P90'].append(f"{stats['p90']:.2f}")
            
            # Create unique identifier for this run+formation combination
            trace_name = f"{bit_model} - {form_name}"
            
            # Add boxplot (top subplot)
            fig.add_trace(
                go.Box(
                    y=segment_data,
                    name=trace_name,
                    marker_color=color,
                    boxmean=True,
                    legendgroup=bit_model,
                    showlegend=False
                ),
                row=1, col=1
            )
    
    # Add table (bottom subplot)
    fig.add_trace(
        go.Table(
            header=dict(
                values=list(stats_data.keys()),
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[stats_data[key] for key in stats_data.keys()],
                align="left",
                font=dict(size=9)
            )
        ),
        row=2, col=1
    )
    
    # Update layout for perfect alignment
    fig.update_layout(
        title=f"{target_column} Distribution by Bit Run and Formation",
        yaxis_title=target_column,
        xaxis_title="Run - Formation Combination",
        xaxis_type='category',
        # boxmode='group',
        height=900,
        margin=dict(t=100, b=100),
        legend_title_text='Bit Model'
    )
    
    fig.show()

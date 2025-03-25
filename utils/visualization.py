import plotly.graph_objects as go
from typing import List

def create_radar_chart(values: List[float], categories: List[str], title: str) -> go.Figure:
    fig = go.Figure()
    # Close the loop for radar chart
    values_closed = values.copy()
    categories_closed = categories.copy()
    if values:
        values_closed.append(values[0])
        categories_closed.append(categories[0])
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        name=title,
        line=dict(color='rgb(67, 147, 195)', width=2),
        fillcolor='rgba(67, 147, 195, 0.2)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0.2, 0.4, 0.6, 0.8],
                ticktext=["0.2", "0.4", "0.6", "0.8"],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                direction='clockwise',
                rotation=90
            )
        ),
        title=dict(
            text=title,
            font=dict(size=14),
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        margin=dict(l=80, r=80, t=60, b=60),
        height=420,
        autosize=True,
        showlegend=False,
    )
    return fig

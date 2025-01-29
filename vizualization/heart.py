import numpy as np

from plotly.graph_objects import (
    Figure,
    Layout,
    Frame,
    Scatter
)


def heart():
    # Creare a periodic function that will draw a heart
    def draw_heart(x, a): return abs(x)**(2/3) + 0.9 * \
        (3.3 - x**2)**0.5 * -np.cos(a*x*np.pi)

    # Set ranges for plot and parameter and then calculate xs and ys for plots
    y_max, y_min = 2.39, -1.562
    x_max, x_min = 1.82, -1.82
    a_min, a_max = 0, 15

    x_aspect = (y_max + abs(y_min)) / (x_max + abs(x_min))

    xs = np.linspace(x_min, x_max, 1000)
    a_param = np.linspace(a_min, a_max, 300)
    ys = [draw_heart(float(x), a) for a in a_param for x in xs]
    ys = np.reshape(ys, (a_param.size, xs.size)).real

    # Create button
    updatemenus = [dict(
        buttons=[dict(
            args=[None, dict(
                frame=dict(duration=0, redraw=False),
                mode='next',
                fromcurrent=True
            )],
            label='❤️️', method='animate'
        )],
        type='buttons', showactive=False,
        direction='right',
        xanchor='center', x=0.5, yanchor='top', y=1,
        bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)'
    )]

    # Configurate layout, first screen and frames
    layout = Layout(
        xaxis=dict(
            constrain='domain', scaleanchor='y', scaleratio=x_aspect, fixedrange=True,
            showgrid=False, zeroline=False, showline=False, showticklabels=False
        ),
        yaxis=dict(
            range=[y_min, y_max], fixedrange=True,
            showgrid=False, zeroline=False, showline=False, showticklabels=False
        ),
        margin=dict(l=450, r=450), plot_bgcolor='rgba(0,0,0,0)', dragmode=False,
        updatemenus=updatemenus

    )

    first_screen = Scatter(x=xs, y=ys[0], line=dict(
        color='rgba(0,0,0,0)'), hoverinfo='skip')

    frames = [
        Frame(data=Scatter(x=xs, y=y, line=dict(color="red", width=3)))
        for y in ys
    ]

    # Create a figure and show it
    fig = Figure(data=first_screen, layout=layout, frames=frames)

    return fig
